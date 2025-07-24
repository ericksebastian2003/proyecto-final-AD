
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, PasswordField
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
    username = StringField('Usuario',validators=[DataRequired()])
    password = PasswordField('Contraseña',validators=[DataRequired()])
    submit = SubmitField('Iniciar sesión')

class ProductForm(FlaskForm):
    nombre = StringField('Nombre',validators=[DataRequired()])
    codigo = StringField('Código',validators=[DataRequired()])
    descripcion = TextAreaField('Descripción',validators=[DataRequired()])
    unidad = StringField('Unidad',validators=[DataRequired()])
    categoria = StringField('Categoria',validators=[DataRequired()])
    submit = SubmitField('Crear producto')
