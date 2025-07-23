from quart import Blueprint, request, jsonify, current_app

from ..core.utils.token_handler import get_info
from ..db.user.user_crud import get_user_or_create

bp = Blueprint("login", __name__)

@bp.route('/login_enter', methods=["GET"])
async def login_enter():

    token = request.headers.get("token-de-autenticacao")

    if not token:
        return jsonify({"error": "Token não fornecido!"}), 400
    
    user_info = await get_info(token)
    matricula = user_info.get("id", None)
    nome = user_info.get("name", None)

    if matricula is None or not matricula:
        return jsonify({"error": "Token inválido ou erro na requisição"}), 403
    
    print(user_info)
    async with current_app.db_pool.acquire() as conn:
        await get_user_or_create(conn, nome, matricula)

    return jsonify(user_info), 200