from quart import Blueprint, request, jsonify, render_template

bp = Blueprint("web", __name__)

@bp.route('/')
async def home():
    # Renderiza a página HTML onde o chatbot será exibido
    return await render_template('index.html')

@bp.route('/login')
async def login():
    # Renderiza a página HTML onde o login será exibido
    return await render_template('login.html')

@bp.route('/politica_termos')
async def politica_termos():
    # Renderiza a página HTML onde o login será exibido
    return await render_template('politica_termos.html')