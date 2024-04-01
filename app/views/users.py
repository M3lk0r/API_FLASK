import sys
import re
from app import db
from flask import jsonify, request, url_for, redirect
from werkzeug.security import generate_password_hash, check_password_hash
from ..models.users import Users, user_schema

def post_user():
    nome = request.json['nome']
    email = request.json['email']
    senha = generate_password_hash(request.json['senha'])

    user = user_by_email(email)
    if user:
        result = user_schema.dump(user)
        return jsonify({'message': 'email already exists', 'data': {}})
    
    user = Users(nome, email, senha)
    
    try:
        if not is_valid_email(email):
            return jsonify({'message': 'Email inválido', 'data': {}}), 400 
        db.session.add(user)
        db.session.commit()
        result = user_schema.dump(user)
        return jsonify({'message': 'Usuário cadastrado com sucesso!', 'data': result}), 201
    except:
        return jsonify({'message': 'Impossivel criar o usuário', 'data': {}}), 500

def user_by_email(email):
    try:
        return Users.query.filter(Users.email == email).one()
    except:
        return None
    

def is_valid_email(email):
    """
    Função que valida um email
    """
    regex = r'^[a-zA-Z0-9+_\-]+(\.[a-zA-Z0-9+_\-]+)*@[a-zA-Z0-9][a-zA-Z0-9-]*(\.[a-zA-Z0-9-]+)*$'
    return True if re.match(regex, email) else False