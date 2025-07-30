from quart import Blueprint, request, jsonify, current_app

from application.config import title_model
from application.db.chat_tab.chat_crud import get_chat_messages_by_chat_id, get_chat_tabs_by_matricula, delete_chat_tab

from ..core.utils.title import generate_chat_title
from ..core.utils.token_handler import get_info

bp = Blueprint("chat", __name__)

@bp.route('/resumir', methods=["POST"])
async def resumir():
    data = await request.get_json()

    if not data or 'texto' not in data:
        return jsonify({"erro": "Campo 'texto' é obrigatório"}), 400

    texto = data['texto']

    try:
        resumo = generate_chat_title(text=texto, llm=title_model)
        return jsonify({"resumo": resumo['titulo']}), 200
    except Exception as e:
        return jsonify({"erro": f"Erro ao gerar resumo: {str(e)}"}), 500

@bp.route('/update_title', methods=["POST"])
async def update_title():
    data = await request.get_json()
    chat_id = data.get('chat_id')
    title = data.get('title')

    if not chat_id or not title:
        return jsonify({"error": "Faltou chat_id ou title"}), 400

    async with current_app.db_pool.acquire() as conn:
        await conn.execute("UPDATE chat_tabs SET title=$1 WHERE id=$2", title, chat_id)

    return jsonify({"ok": True})

@bp.route('/delete_chat', methods=["POST"])
async def delete_chat():
    data = await request.get_json()
    chat_id = data.get("chat_id")

    print("ID RECEBIDO PARA DELETAR: ", chat_id)

    if not chat_id:
        return jsonify({"error": "chat_id não fornecido"}), 400
    
    async with current_app.db_pool.acquire() as conn:
        await delete_chat_tab(conn, chat_id)
    
    await current_app.checkpointer.adelete_thread(chat_id) # também deleta os checkpoints do PostgresSaver

    return jsonify({"msg": f"Chat {chat_id} deletado"}), 200

@bp.route("/get_chat", methods=["POST"])
async def get_chat():
    data = await request.json
    chat_id = data.get("chat_id")
    token = data.get("token")

    if not token:
        return jsonify({"data": []})
    
    user_info = await get_info(token)
    matricula = str(user_info.get("id", None))

    if not matricula:
        return jsonify({"data": []})
    
    async with current_app.db_pool.acquire() as conn:
        # garantir que o chat pertence ao usuário
        rows = await conn.fetch("""
            SELECT ct.id
            FROM chat_tabs ct
            JOIN users u ON ct.user_id = u.id
            WHERE ct.id = $1 AND u.matricula = $2
        """, chat_id, matricula)

        if not rows:
            return jsonify({"data": []})

        messages = await get_chat_messages_by_chat_id(conn, chat_id)
    
    print("entrou no get_chat:\n", messages)
    
    result = []
    for msg in messages:
        timestamp = msg["created_at"].isoformat()
        if msg["role"] == "human_message":
            result.append({"human_message": msg["content"], "timestamp": timestamp})
        elif msg["role"] == "ai_message":
            result.append({"ai_message": msg["content"], "timestamp": timestamp})
    print("\nChat encontrado: ", result)
    return jsonify({"data": result})

@bp.route("/get_historico", methods=["POST"])
async def get_historico():
    data = await request.get_json()
    token = data.get("token")

    if not token:
        return jsonify({"error": "Token não fornecido!"}), 400

    user_info = await get_info(token)
    matricula = str(user_info.get("id", None))

    if not matricula:
        return jsonify({"error": "Token inválido ou erro na requisição"}), 403
    
    async with current_app.db_pool.acquire() as conn:
        tabs = await get_chat_tabs_by_matricula(conn, matricula)

    print("entrou no get_historico:\n", tabs)
    if not tabs:
        return jsonify([])
    
    result = [
        {
            "chat_id": str(tab["id"]), 
            "title": tab["title"],
            "updated_at": tab["updated_at"].isoformat() if tab["updated_at"] else None
        }
        for tab in tabs
    ]
    print("\nValor dos chats retornado:\n", result)
    return jsonify(result)