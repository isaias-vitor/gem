from flask import *

from .database import SupabaseClient
from .forms import *

routes = Blueprint('routes', __name__)

# Rota Protegida
@routes.route('/dashboard')
@login_required
def dashboard():
    return f"Bem-vindo ao painel"