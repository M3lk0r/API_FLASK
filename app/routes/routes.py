from app import app
from flask import jsonify, url_for, redirect
from ..views import users, helper

@app.route('/', methods=['GET'])
@helper.token_required
def root(current_user):
    return jsonify({'message': f'Hello {current_user.name}'})


@app.route('/authenticate', methods=['POST'])
def authenticate():
    return helper.auth()

@app.route('/users', methods=['POST'])
def cadastro():
    return users.post_user()
