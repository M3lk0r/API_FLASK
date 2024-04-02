import datetime
from app import db, ma, app

"""Definição da classe/tabela dos usuários e seus campos"""
class Users(db.Model):
    __tablename__ = 'usuarios'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(60), nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    senha = db.Column(db.String(200), nullable=False)
    genero = db.Column(db.String(10), nullable=False)
    telefone = db.Column(db.String(20), nullable=False)
    estado = db.Column(db.String(20), nullable=False)
    cidade = db.Column(db.String(20), nullable=False)
    funcao = db.Column(db.String(10), default="paciente")
    created_on = db.Column(db.DateTime, default=datetime.datetime.now())
    
    def __init__(self, nome, email, senha, genero, telefone, estado, cidade):
        self.nome = nome
        self.email = email
        self.senha = senha
        self.genero = genero
        self.telefone = telefone
        self.estado = estado
        self.cidade = cidade


"""Definindo o Schema do Marshmallow para facilitar a utilização de JSON"""
class UsersSchema(ma.Schema):
    class Meta:
        fields = ('id', 'nome', 'email', 'senha', 'genero', 'telefone', 'estado', 'cidade', 'funcao', 'created_on')


user_schema = UsersSchema()
#users_schema = UsersSchema(strict=True, many=True)
users_schema = UsersSchema(many=True)

"""Cria tabela a partir do Schema definido"""
with app.app_context():
    db.create_all()