from quart import Blueprint, request, jsonify, current_app
from langchain_core.messages import HumanMessage

from ..core.utils.file_handler.handler import realizar_tratamento_dos_arquivos

bp = Blueprint("message", __name__)

@bp.route('/chat', methods=["POST"])
async def message():
    # Recebe a mensagem do usuário
    form = await request.form
    files = await request.files
    user_message = form.get("input_data")
    profile_raw = form.get("profile")
    arquivos = files.getlist('archives[]')

    print(profile_raw)

    if len(arquivos) > 0:
        user_message = f"{user_message}\n\n{realizar_tratamento_dos_arquivos(arquivos)}"

    config = {"configurable": {"thread_id": "1"}}
    inputs = {"messages": [HumanMessage(content=user_message)]}
    response = []

    try:
        async for chunk in current_app.system.astream(inputs, config=config, stream_mode="values"):
            chunk["messages"][-1].pretty_print()
            response.append(chunk["messages"][-1].content)
        print(config)
        print(await current_app.system.aget_state(config))
        return jsonify({"response": response[-1] if response else "Desculpe, erro interno."})
    except Exception as e:
        return jsonify({"response": f"Erro: {str(e)}"}), 500