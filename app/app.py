from flask import *
from dotenv import load_dotenv
from os import getenv


from database import *
from routes import routes
# import forms


# Carregamento do arquivo .env
load_dotenv()

# App Flask
app = Flask(__name__)
app.register_blueprint(routes)
app.config['SECRET_KEY'] = getenv('SECRET_KEY_APP')

