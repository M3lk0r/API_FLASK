import datetime
import jwt
from functools import wraps
from app import app
from flask import request, jsonify
from werkzeug.security import check_password_hash
from .users import user_by_email

def token_required(fn):
    """
    Decorador para proteger uma rota, verificando se o token JWT é válido
    """
    @wraps(fn)
    def decorated(*args, **kwargs):
        token = None
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            token = auth_header.split(" ")[1]
            
        if not token:
            return jsonify({"message": "Token is missing"}), 401
        
        try:
            payload = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
            print (payload)
            
        except jwt.ExpiredSignatureError:
            return jsonify({"message": "Token expired"}), 401
        
        except jwt.InvalidTokenError:
            return jsonify({"message": "Invalid token"}), 401
        
        user = user_by_email(payload['email'])
        if not user:
            return jsonify({"message": "User not found"}), 401
        
        return fn(user, *args, **kwargs)
    return decorated

def auth():
    auth = request.authorization

    if not auth or not auth.username or not auth.password:
        return jsonify({'message': 'could not verify', 'WWW-Authenticate': 'Basic realm="Login required"'}), 401

    user = user_by_email(auth.username)
    if not user:
        return jsonify({'message': 'user not found', 'data': []}), 401

    if user and check_password_hash(user.password, auth.password):
        token = jwt.encode({'email': user.email, 'exp': datetime.datetime.now() + datetime.timedelta(hours=12) }, app.config['SECRET_KEY'])
        return jsonify({'message': 'Validated successfully', 'token': token, 'exp': datetime.datetime.now() + datetime.timedelta(hours=12)}), 200

    return jsonify({'message': 'Invalid credentials', 'WWW-Authenticate': 'Basic realm="Login required"'}), 401
