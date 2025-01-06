from flask import *
from database import SupabaseClient

# Chamando banco de dados
db = SupabaseClient()

routes = Blueprint('routes', __name__)

# Página Principal
@routes.route('/')
def index():
    teste = db.primeiraBusca()
    return render_template('index.html', teste=teste)