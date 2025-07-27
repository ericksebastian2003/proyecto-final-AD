from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField, FloatField, TextAreaField, SelectField
from wtforms.validators import DataRequired, Length, Email, NumberRange

class LoginForm(FlaskForm):
    correo = StringField('Correo', validators=[DataRequired(), Email()])
    contraseña = PasswordField('Contraseña', validators=[DataRequired(), Length(min=6)])
    submit = SubmitField('Iniciar sesión')

class RegisterForm(FlaskForm):
    nombre = StringField('Nombre', validators=[DataRequired(), Length(min=2, max=100)])
    correo = StringField('Correo', validators=[DataRequired(), Email()])
    contraseña = PasswordField('Contraseña', validators=[DataRequired(), Length(min=6)])
    rol = SelectField('Rol', choices=[('admin', 'Administrador'), ('cajero', 'Cajero')], validators=[DataRequired()])
    submit = SubmitField('Registrar')

class ProductForm(FlaskForm):
    nombre = StringField('Nombre', validators=[DataRequired()])
    codigo = StringField('Código', validators=[DataRequired()])
    descripcion = TextAreaField('Descripción', validators=[DataRequired()])
    unidad = StringField('Unidad', validators=[DataRequired()])
    categoria = StringField('Categoría', validators=[DataRequired()])
    stock = IntegerField('Stock', validators=[DataRequired(), NumberRange(min=0)])
    precio = FloatField('Precio', validators=[DataRequired(), NumberRange(min=0)])
    submit = SubmitField('Agregar Producto')
