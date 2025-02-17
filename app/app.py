from flask import Flask, render_template, redirect, url_for, flash, request, session
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from datetime import timedelta

from .routes import routes
from .forms import *
from .database import SupabaseClient

app = Flask(__name__)
app.register_blueprint(routes)
app.secret_key = 'truco'
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=30)  # Sessão permanente por 30 dias


# Configuração do Flask-Login
login_manager = LoginManager(app)
login_manager.login_view = 'login'  # Redireciona para a página de login se não autenticado

# Definindo o comportamento do login
@app.before_request
def make_session_permanent():
    session.permanent = True  # Faz a sessão ser permanente


# Modelo de usuário
class User(UserMixin):
    def __init__(self, data):
        self.id = data['id']  # Flask-Login exige que o atributo seja `id`
        self.username = data['nome']  # Nome do usuário
        self.nivel = data['nivel']  # Nível do usuário
    
    def __repr__(self):
        return f'<User {self.username}>'

# Carregar usuário pelo Flask-Login usando os dados armazenados na sessão
@login_manager.user_loader
def load_user(user_id):
    user_data = session.get('user_data')  # Recupera os dados do usuário da sessão
    if user_data and str(user_data['id']) == str(user_id):
        return User(user_data)  # Retorna um objeto User reconstruído
    return None  # Retorna None se o usuário não estiver na sessão

# Rota de Login
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        try_login = SupabaseClient().userLogin(username, password)  # Verifica no banco

        if try_login:
            user = User(try_login)  # Cria um objeto User
            login_user(user)  # Registra o usuário no Flask-Login

            # Armazena os dados do usuário na sessão
            session['user_data'] = {
                'id': try_login['id'],
                'nome': try_login['nome'],
                'nivel': try_login['nivel']
            }

            if try_login['nivel'] == 'instrutor':
                students = SupabaseClient().seekStudents()
                session['students'] = students
                session['act_student'] = {}

            flash('Login realizado com sucesso!', 'success')
            return redirect(url_for('routes.ficha'))
        else:
            flash('Credenciais inválidas, tente novamente.', 'danger')
    
    return render_template('login.html', form=form)

# Rota de Logout
@app.route('/logout')
def logout():
    logout_user()
    session.pop('user_data', None)  # Remove os dados da sessão ao deslogar
    flash('Você saiu da conta.', 'info')
    return redirect(url_for('login'))

# Página inicial (redireciona para login)
@app.route('/')
def home():
    return redirect(url_for('login'))

# Dashboard de exemplo
@app.route('/dashboard')
@login_required
def dashboard():
    return f"Bem-vindo, {current_user.username}! Seu ID é {current_user.id}. Seu nível é {current_user.nivel}."

if __name__ == '__main__':
    app.run(debug=True)
