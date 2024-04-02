import sys
import re
from app import db
from flask import jsonify, request, url_for, redirect
from werkzeug.security import generate_password_hash, check_password_hash
from ..models.users import Users, user_schema, users_schema

def post_user():
    nome = request.json['nome']
    email = request.json['email']
    senha = generate_password_hash(request.json['senha'])
    genero = request.json['genero']
    telefone = request.json['telefone']
    estado = request.json['estado']
    cidade = request.json['cidade']
    
    user = user_by_email(email)
    if user:
        result = user_schema.dump(user)
        return jsonify({'message': 'email already exists', 'data': {}})
    
    user = Users(nome, email, senha, genero, telefone, estado, cidade)
    
    try:
        if not is_valid_email(email):
            return jsonify({'message': 'Email inválido', 'data': {}}), 400 
        db.session.add(user)
        db.session.commit()
        result = user_schema.dump(user)
        return jsonify({'message': 'Usuário cadastrado com sucesso!', 'data': result}), 201
    except:
        return jsonify({'message': 'Impossivel criar o usuário', 'data': {}}), 500

def get_user(id):
    user = Users.query.get(id)
    if not user:
        return jsonify({'message': 'Usuário não encontrado', 'data': {}}), 404
    result = user_schema.dump(user)
    return jsonify({'message': 'Usuário encontrado', 'data': result}), 200


def get_users():
    users = Users.query.all()
    result = users_schema.dump(users)
    return jsonify({'message': 'Usuários encontrados', 'data': result}), 200

def update_user(id):
    user = Users.query.get(id)
    if not user:
        return jsonify({'message': 'Usuário não encontrado', 'data': {}}), 404

    nome = request.json.get('nome', user.nome)
    email = request.json.get('email', user.email)
    senha = request.json.get('senha', user.senha)
    genero = request.json['genero']
    telefone = request.json['telefone']
    estado = request.json['estado']
    cidade = request.json['cidade']

    if senha:
        senha = generate_password_hash(senha)

    try:
        if email and not is_valid_email(email):
            return jsonify({'message': 'Email inválido', 'data': {}}), 400 
        user.nome = nome
        user.email = email
        if senha:
            user.senha = senha
        user.genero = genero
        user.telefone = telefone
        user.estado = estado
        user.cidade = cidade
        db.session.commit()
        result = user_schema.dump(user)
        return jsonify({'message': 'Usuário atualizado com sucesso!', 'data': result}), 200
    except:
        return jsonify({'message': 'Impossivel atualizar o usuário', 'data': {}}), 500

def delete_user(id):
    user = Users.query.get(id)
    if not user:
        return jsonify({'message': 'Usuário não encontrado', 'data': {}}), 404

    try:
        db.session.delete(user)
        db.session.commit()
        return jsonify({'message': 'Usuário deletado com sucesso!', 'data': {}}), 200
    except:
        return jsonify({'message': 'Impossivel deletar o usuário', 'data': {}}), 500

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