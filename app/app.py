from flask import Flask, render_template, redirect, url_for, flash, request, session
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from datetime import timedelta
import os

from .routes import routes
from .forms import *
from .database import SupabaseClient

def create_app():
    app = Flask(__name__)
    app.register_blueprint(routes)
    
    # Usar variável de ambiente para a secret key em produção
    app.secret_key = os.environ.get('SECRET_KEY', 'truco')
    app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=30)

    # Configuração do Flask-Login
    login_manager = LoginManager(app)
    login_manager.login_view = 'login'

    # Modelo de usuário
    class User(UserMixin):
        def __init__(self, data):
            self.id = data['id']
            self.username = data['nome']
            self.nivel = data['nivel']
        
        def __repr__(self):
            return f'<User {self.username}>'

    @login_manager.user_loader
    def load_user(user_id):
        user_data = session.get('user_data')
        if user_data and str(user_data['id']) == str(user_id):
            return User(user_data)
        return None

    @app.before_request
    def make_session_permanent():
        session.permanent = True

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        form = LoginForm()
        if form.validate_on_submit():
            username = form.username.data
            password = form.password.data
            try_login = SupabaseClient().userLogin(username, password)

            if try_login:
                user = User(try_login)
                login_user(user)

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

    @app.route('/logout')
    def logout():
        logout_user()
        session.pop('user_data', None)
        flash('Você saiu da conta.', 'info')
        return redirect(url_for('login'))

    @app.route('/')
    def home():
        return redirect(url_for('login'))

    @app.route('/dashboard')
    @login_required
    def dashboard():
        return f"Bem-vindo, {current_user.username}! Seu ID é {current_user.id}. Seu nível é {current_user.nivel}."

    return app

# Criação da instância do app
app = create_app()