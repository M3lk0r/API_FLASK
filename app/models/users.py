import datetime
from app import db, ma, app

"""Definição da classe/tabela dos usuários e seus campos"""
class Users(db.Model):
    __tablename__ = 'usuarios'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(60), nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    created_on = db.Column(db.DateTime, default=datetime.datetime.now())
    
    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self.password = password


"""Definindo o Schema do Marshmallow para facilitar a utilização de JSON"""
class UsersSchema(ma.Schema):
    class Meta:
        fields = ('id', 'username', 'name', 'email', 'password', 'created_on')


user_schema = UsersSchema()
users_schema = UsersSchema(strict=True, many=True)

"""Cria tabela a partir do Schema definido"""
with app.app_context():
    db.create_all()