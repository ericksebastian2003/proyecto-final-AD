from flask import Flask, render_template, redirect, url_for, flash, request
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from dotenv import load_dotenv
import os
from datetime import datetime
from models import db, User, Product, Venta, DetalleVenta
from forms import LoginForm, RegisterForm, ProductForm

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('FLASK_SECRET_KEY')

DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_HOST = os.getenv('DB_HOST')
DB_NAME = os.getenv('DB_NAME')

app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql://{DB_USER}@{DB_HOST}/{DB_NAME}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

login_manager = LoginManager(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
@app.route('/historial')
@login_required
def historial():
    ventas = Venta.query.order_by(Venta.fecha.desc()).all()
    return render_template('historial.html', ventas=ventas)

@app.route('/ventas', methods=['GET', 'POST'])
@login_required
def ventas():
    productos = Product.query.filter(Product.stock > 0).all()  # solo productos con stock disponible

    if request.method == 'POST':
        # Crear la venta
        nueva_venta = Venta(
            usuario_id=current_user.id,
            fecha=datetime.now(),
            forma_pago=request.form.get('forma_pago', 'efectivo'),
            total=0
        )
        db.session.add(nueva_venta)
        db.session.flush()  # para obtener el id de la venta antes del commit

        total_venta = 0
        for producto in productos:
            cantidad_str = request.form.get(f'cantidad_{producto.id}', '0')
            try:
                cantidad = int(cantidad_str)
            except ValueError:
                cantidad = 0

            if cantidad > 0:
                if producto.stock < cantidad:
                    flash(f'No hay suficiente stock para {producto.nombre}.')
                    db.session.rollback()
                    return redirect(url_for('ventas'))

                # Restar stock
                producto.stock -= cantidad

                # Crear detalle venta
                detalle = DetalleVenta(
                    venta_id=nueva_venta.id,
                    producto_id=producto.id,
                    cantidad=cantidad,
                    precio_unitario=producto.precio
                )
                db.session.add(detalle)

                total_venta += producto.precio * cantidad

        if total_venta == 0:
            flash('Debe seleccionar al menos un producto para vender.')
            db.session.rollback()
            return redirect(url_for('ventas'))

        nueva_venta.total = total_venta
        db.session.commit()

        flash(f'Venta registrada correctamente. Total: ${total_venta:.2f}')
        return redirect(url_for('dashboard'))

    return render_template('ventas.html', productos=productos)

@app.route('/', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        correo = form.correo.data
        contraseña = form.contraseña.data

        user = User.query.filter_by(correo=correo).first()
        if user and check_password_hash(user.contraseña, contraseña):
            login_user(user)
            flash('Bienvenido, ' + user.nombre)
            return redirect(url_for('dashboard'))
        else:
            flash('Correo o contraseña incorrectos')
    return render_template('login.html', form=form)

@app.route('/registrar_usuario', methods=['GET', 'POST'])
def registrar_usuario():
    form = RegisterForm()
    if form.validate_on_submit():
        nombre = form.nombre.data
        correo = form.correo.data
        contraseña = form.contraseña.data
        rol = form.rol.data

        if User.query.filter_by(correo=correo).first():
            flash('Correo ya registrado')
            return redirect(url_for('registrar_usuario'))

        hash_pass = generate_password_hash(contraseña)
        nuevo_usuario = User(nombre=nombre, correo=correo, contraseña=hash_pass, rol=rol)
        db.session.add(nuevo_usuario)
        db.session.commit()

        flash('Usuario registrado correctamente, por favor inicia sesión.')
        return redirect(url_for('login'))

    return render_template('registrar_usuario.html', form=form)

@app.route('/dashboard')
@login_required
def dashboard():
    productos = Product.query.all()
    return render_template('dashboard.html', productos=productos, usuario=current_user)

@app.route('/productos', methods=['GET', 'POST'])
@login_required
def productos():
    form = ProductForm()
    if form.validate_on_submit():
        producto = Product(
            nombre=form.nombre.data,
            codigo=form.codigo.data,
            descripcion=form.descripcion.data,
            unidad=form.unidad.data,
            categoria=form.categoria.data,
            stock=form.stock.data,
            precio=form.precio.data,
            disponible=True
        )
        db.session.add(producto)
        db.session.commit()
        flash('Producto agregado correctamente.')
        return redirect(url_for('productos'))

    lista_productos = Product.query.all()
    return render_template('productos.html', form=form, productos=lista_productos)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Has cerrado sesión.')
    return redirect(url_for('login'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
