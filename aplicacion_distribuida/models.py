from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()

class User(UserMixin , db.Model):
    id = db.Column(db.Integer , primary_key = True)
    username = db.Column(db.String(50), unique = True)
    password = db.Column(db.String(100))
class Product(db.Model):
    id = db.Column(db.Integer , primary_key=True)
    nombre = db.Column(db.String(100))
    codigo = db.Column(db.String(50), unique = True)
    descripcion = db.Column(db.Text)
    unidad = db.Column(db.Integer)
    categoria = db.Column(db.String(50))
    disponible = db.Column(db.Boolean)