from flask_wtf import FlaskForm
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length


# Formulário de Login usando Flask-WTF
class LoginForm(FlaskForm):
    username = StringField('Usuário', validators=[DataRequired(), Length(min=2, max=20)])
    password = PasswordField('Senha', validators=[DataRequired()])
    submit = SubmitField('Entrar')