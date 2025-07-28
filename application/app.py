# app.py
import asyncio, asyncpg, sys, uuid
from quart import Quart
from dotenv import load_dotenv

from .routes import chat, message, web, audio, login
from .db.saver import get_postgres_saver
from .db.user.user_crud import get_user_or_create
from .db.chat_tab.chat_crud import *
from .core.system import build_system
from .core.utils.token_handler import get_info
from application.config import DB_URI
from demo.utils.eureca_chat_utils import SocketIOStreamingHandler

load_dotenv(override=True)

if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

app = Quart(__name__, static_url_path="/static", template_folder="templates")

# Socket.IO
import socketio

sio = socketio.AsyncServer(async_mode="asgi", cors_allowed_origins="*")
sio_app = socketio.ASGIApp(sio, app)

# Variáveis globais
app.system = None
app.checkpointer_cm = None

@app.before_serving
async def setup():
    # Inicializa o checkpointer
    app.checkpointer_cm = get_postgres_saver(db_uri=DB_URI)
    app.checkpointer = await app.checkpointer_cm.__aenter__()

    # Usar setup() apenas na primeira execução do sistema, para criar as tabelas do PostgresSaver
    await app.checkpointer.setup()
    # await app.checkpointer.adelete_thread("anon_8de0f045-4617-4510-8481-221356e93502")

    # Inicializa a pool do asyncpg, para lidar com as demais tabelas do sistema
    app.db_pool = await asyncpg.create_pool(dsn=DB_URI)

    # Inicializa o chat
    app.system = build_system(app.checkpointer)

@app.after_serving
async def shutdown():
    await app.checkpointer_cm.__aexit__(None, None, None)
    await app.db_pool.close()

# Routes
app.register_blueprint(audio.bp)
app.register_blueprint(chat.bp)
app.register_blueprint(message.bp)
app.register_blueprint(web.bp)
app.register_blueprint(login.bp)

# Execução com Hypercorn (socketio), rodar no bash:
# hypercorn application.app:sio_app
# hypercorn application.app:sio_app --reload

# Execução normal (sem socketio):
# if __name__ == "__main__":
#     app.run(debug=True)

from langchain_core.messages import HumanMessage
from .core.utils.file_handler.handler import realizar_tratamento_dos_arquivos

anon_sessions = {}

@sio.on('connect')
async def connect(sid, environ):
    print(f"[SOCKET] Cliente conectado: {sid}")
    anon_thread_id = f"anon_{uuid.uuid4()}"
    anon_sessions[sid] = anon_thread_id
    print(f"Thread_id anônimo criado para sid={sid}: {anon_thread_id}")

@sio.on('disconnect')
async def disconnect(sid):
    print(f"[SOCKET] Cliente desconectado: {sid}")
    thread_id = anon_sessions.pop(sid, None)
    if thread_id and thread_id.startswith("anon_"):
        print(f"Deletando checkpoint anônimo: {thread_id}")
        await app.checkpointer.adelete_thread(thread_id)

@sio.on('input_text')
async def handle_input(sid, data):
    print(data)
    user_message = data.get('input_data')
    arquivos = data.get('arquivos', [])
    token = data.get('token')
    chat_id = data.get('chat_id')

    print("TOKEN: ", token)
    print("CHAT_ID:", chat_id)

    if not token:
        anon_thread_id = anon_sessions.get(sid)
        asyncio.create_task(execute_system(sid, user_message, arquivos, token, anon_thread_id))
    else:
        asyncio.create_task(execute_system(sid, user_message, arquivos, token, chat_id))

async def execute_system(sid, user_message, arquivos, token, chat_tab_id):
    try:
        if token:
            if not chat_tab_id:
                user_info = await get_info(token)
                matricula = str(user_info.get("id"))
                nome = user_info.get("name", None)

                if not matricula:
                    await sio.emit("resposta_final", {"resposta": "Usuário inválido"}, room=sid)
                    return
            
                async with app.db_pool.acquire() as conn:
                    user = await get_user_or_create(conn, nome, matricula)
                    chat_tab = await create_chat_tab(conn, user["id"], "Novo Chat")
                    chat_tab_id = str(chat_tab["id"])
        
        print("\nCHAT TAB ID: ", chat_tab_id)

        config = {
            "configurable": {"thread_id": chat_tab_id}, # thread_id é o id do chat_tab gerado ao ser criado no bd, caso não tenha usuário logado é um id gerado temporariamente
            "token": token,
            "callbacks_sio": [SocketIOStreamingHandler(sid=sid, socketio=sio)]
        }
        
        await sio.emit("status", {"resposta": "Iniciando os agentes..."})

        if arquivos and isinstance(arquivos, list) and len(arquivos) > 0:
            await sio.emit("status", {"resposta": "Lendo arquivos pdf..."}, room=sid)
            user_message = f"Texto contido nos arquivos lidos: {realizar_tratamento_dos_arquivos(arquivos)}. \n\n Pergunta: {user_message}."
        
        inputs = {"messages": [HumanMessage(content=user_message)]}
        response = ""

        async for chunk in app.system.astream(inputs, config, stream_mode="values"):
            print("\n\nCHUNK GERADA: ", chunk["messages"][-1])
            chunk["messages"][-1].pretty_print()
            response = chunk["messages"][-1].content
        response = response or "Desculpe, não consegui processar sua solicitação."

        if token:
            async with app.db_pool.acquire() as conn:
                await add_chat_message(conn, chat_tab_id, "human_message", user_message)
                await add_chat_message(conn, chat_tab_id, "ai_message", response)
            await sio.emit("resposta_final", {"resposta": response, "chat_id": chat_tab_id}, room=sid)
        else:
            await sio.emit("resposta_final", {"resposta": response}, room=sid)

    except Exception as e:
        await sio.emit("resposta_final", {"resposta": f"Erro: {str(e)}"}, room=sid)