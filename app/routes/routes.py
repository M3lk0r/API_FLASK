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

@app.route('/users/<int:user_id>', methods=['PUT'])
@helper.token_required
def atualizar_usuario(user_id):
    return users.update_user(user_id)

@app.route('/users/<int:user_id>', methods=['DELETE'])
@helper.token_required
def deletar_usuario(user_id):
    return users.delete_user(user_id)

@app.route('/users/<int:user_id>', methods=['GET'])
@helper.token_required
def get_user(user_id):
    return users.get_user(user_id)

@app.route('/users', methods=['GET'])
@helper.token_required
def get_users():
    return users.get_users()

