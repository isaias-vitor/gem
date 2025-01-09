from flask import Flask, render_template, redirect, url_for, flash, request
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user

from .routes import routes

app = Flask(__name__)
app.register_blueprint(routes)
app.secret_key = 'truco'

# Configuração do Flask-Login
login_manager = LoginManager(app)
login_manager.login_view = 'login'  # Redireciona para a página de login se não autenticado

# Simulação de banco de dados
users_db = {
    "admin": {"password": "1234"}
}

# Modelo de usuário
class User(UserMixin):
    def __init__(self, username):
        self.id = username

# Carregar usuário pelo Flask-Login
@login_manager.user_loader
def load_user(user_id):
    if user_id in users_db:
        return User(user_id)
    return None

# Formulário de Login usando Flask-WTF
class LoginForm(FlaskForm):
    username = StringField('Usuário', validators=[DataRequired(), Length(min=2, max=20)])
    password = PasswordField('Senha', validators=[DataRequired()])
    submit = SubmitField('Entrar')

# Rota de Login
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        if username in users_db and users_db[username]["password"] == password:
            user = User(username)
            login_user(user)
            flash('Login realizado com sucesso!', 'success')
            return redirect(url_for('routes.dashboard'))
        else:
            flash('Credenciais inválidas, tente novamente.', 'danger')
    return render_template('login.html', form=form)

# Rota de Logout
@app.route('/logout')
def logout():
    logout_user()
    flash('Você saiu da conta.', 'info')
    return redirect(url_for('login'))

# Página inicial (redireciona para login)
@app.route('/')
def home():
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
