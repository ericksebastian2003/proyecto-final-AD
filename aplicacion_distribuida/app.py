from flask import Flask, render_template, redirect, url_for, flash, request
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from models import db, User, Product
from forms import LoginForm, ProductForm
import os
from dotenv import load_dotenv
# Cargar variables de entorno
load_dotenv()  
app = Flask(__name__)

# Configuración de la base de datos
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_HOST = os.getenv('DB_HOST')
DB_NAME = os.getenv('DB_NAME')

# URI de conexión a la base de datos
app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql://{DB_PASSWORD}@{DB_HOST}/{DB_NAME}'
 
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = os.getenv('FLASK_SECRET_KEY')

# Inicialización de la base de datos y login manager
db.init_app(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.password == form.password.data:
            login_user(user)
            return redirect(url_for('dashboard'))
        flash('Usuario o contraseña incorrectos')
    return render_template('login.html', form=form)

@app.route('/dashboard')
@login_required
def dashboard():
    productos = Product.query.all()
    return render_template('dashboard.html', productos=productos)

@app.route('/agregar', methods=['GET', 'POST'])
@login_required
def agregar_producto():
    form = ProductForm()
    if form.validate_on_submit():
        if Product.query.filter_by(codigo=form.codigo.data).first():
            flash('Ya existe un producto con ese código')
        else:
            nuevo = Product(
                nombre=form.nombre.data,
                codigo=form.codigo.data,
                descripcion=form.descripcion.data,
                unidad=form.unidad.data,
                categoria=form.categoria.data,
                disponible=True
            )
            db.session.add(nuevo)
            db.session.commit()
            flash('Producto agregado exitosamente')
            return redirect(url_for('dashboard'))
    return render_template('productos.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
