from flask_wtf import FlaskForm
from wtforms.fields import StringField, PasswordField, SubmitField, IntegerField
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
  usuario= StringField('Usuario',validators=[DataRequired()])
  password= PasswordField('Password',validators=[DataRequired()])
  submit= SubmitField('Login')

class BiografiaForm(FlaskForm):
  nombre = StringField('Nombre', validators=[DataRequired()])
  resumen = StringField('Resumen')
  rol = StringField('Rol', validators=[DataRequired()])
  foto = StringField('Foto', validators=[DataRequired()])
  ubicacion = StringField('Ubicación', validators=[DataRequired()])
  cv = StringField('C.V.')
  github = StringField('GitHub', validators=[DataRequired()])
  twitter = StringField('Twitter', validators=[DataRequired()])
  submit= SubmitField('Actualizar Biografia')

class ProyectosForm(FlaskForm):
  codigo = IntegerField('Código', validators=[DataRequired()])
  descripcion = StringField('Descripcion', validators=[DataRequired()])
  imagen = StringField('Imagen', validators=[DataRequired()])
  nombre = StringField('Nombre', validators=[DataRequired()])
  url = StringField('URL', validators=[DataRequired()])
  submit= SubmitField('Actualizar Proyecto')
