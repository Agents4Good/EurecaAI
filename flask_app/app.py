import asyncio, json, sys, socketio
import speech_recognition as sr

# ASYNCIO Event Loop para windows
if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

from quart import Quart, request, jsonify, render_template
from langgraph.checkpoint.postgres.aio import AsyncPostgresSaver
from demo.agents.eureca_chat import EurecaChat
from .utils.langchain_models import supervisor_model, aggregator_model, agents_model
from langchain_core.messages import HumanMessage
from langchain_core.callbacks.base import BaseCallbackHandler

from io import BytesIO
from pydub import AudioSegment
from langchain_community.chat_models import ChatDeepInfra

from .utils.db_path import *
from .utils.file_handler.handler import realizar_tratamento_dos_arquivos

from dotenv import load_dotenv

load_dotenv(override=True)

app = Quart(__name__, static_url_path="/static", template_folder="templates")
sio = socketio.AsyncServer(async_mode="asgi", cors_allowed_origins="*", max_http_buffer_size=100_000_000)
sio_app = socketio.ASGIApp(sio, app)  # app final para rodar com Hypercorn

system = None # EurecaChat
checkpointer = None # PostgresSaver Checkpointer

@app.before_serving
async def setup():
    global system, checkpointer
    #checkpointer_cm = AsyncPostgresSaver.from_conn_string(DB_URI)
    #app.checkpointer_cm = checkpointer_cm
    #checkpointer = await checkpointer_cm.__aenter__()

    #await checkpointer.setup()
    #await checkpointer.adelete_thread("1")

    # Inicializando instância do EurecaChat
    system = EurecaChat(
        supervisor_model=supervisor_model,
        aggregator_model=aggregator_model,
        agents_model=agents_model,
        #checkpointer=checkpointer
    ).build()

@app.after_serving
async def shutdown():
    await app.checkpointer_cm.__aexit__(None, None, None)

@app.route('/')
async def home():
    # Renderiza a página HTML onde o chatbot será exibido
    return await render_template('index.html')

@app.route('/login')
async def login():
    # Renderiza a página HTML onde o login será exibido
    return await render_template('login.html')

@app.route('/politica_termos')
async def politica_termos():
    # Renderiza a página HTML onde o login será exibido
    return await render_template('politica_termos.html')

@app.route('/delete_chat', methods=["POST"])
async def delete_chat():
    return jsonify({"msg": "apagado"}), 200

@app.route('/resumir', methods=["POST"])
async def resumir():
    data = await request.get_json()

    if not data or 'texto' not in data:
        return jsonify({"erro": "Campo 'texto' é obrigatório"}), 400

    texto = data['texto']

    try:
        llm = ChatDeepInfra(model="meta-llama/Meta-Llama-3.1-8B-Instruct", temperature=0)
        resposta = llm.invoke(
            f"""
            "Gere um título de até 3 palavras para o texto a seguir:
            {texto}
            
            *IMPORTANTE*:
            - Você sempre deve gerar um título, não faça nada além disso.
            - Sempre gere no seguinte formato: {{"titulo": "titulo_gerado"}}
            """
        )
        print("RESUMO PARA O TÍTULO: ", resposta)
        resumo = resposta.content if hasattr(resposta, "content") else str(resposta)
        resumo = resumo.replace("'", '"')
        resumo = json.loads(resumo)
        return jsonify({"resumo": resumo['titulo']}), 200
    except Exception as e:
        return jsonify({"erro": f"Erro ao gerar resumo: {str(e)}"}), 500

@app.route('/chat', methods=['POST'])
async def chat():
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
        async for chunk in system.astream(inputs, config=config, stream_mode="values"):
            chunk["messages"][-1].pretty_print()
            response.append(chunk["messages"][-1].content)
        return jsonify({"response": response[-1] if response else "Desculpe, erro interno."})
    except Exception as e:
        return jsonify({"response": f"Erro: {str(e)}"}), 500

@app.route("/voice-to-text", methods=["POST"])
async def voice_to_text():
    form = await request.files
    if 'file' not in form:
        return jsonify({"error": "No file part"}), 400
    
    print(form)
    audio_file = form['file']

    if audio_file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    
    audio_seg = AudioSegment.from_file(audio_file)
    wav_io = BytesIO()
    audio_seg.export(wav_io, format='wav')
    wav_io.seek(0)

    r = sr.Recognizer()
    with sr.AudioFile(wav_io) as source:
        audio_dt = r.record(source)
    try:
        txt = r.recognize_google(audio_dt, language="pt-BR")
        print(f"Transcrição: {txt}")
        return jsonify({"transcription": txt}), 200
    except sr.UnknownValueError:
        return jsonify({"error": "Não foi possível entender o áudio"}), 400
    except sr.RequestError as e:
        return jsonify({"error": f"Erro ao tentar usar o serviço de reconhecimento de fala: {e}"}), 500

# Handler de streaming para tokens
class SocketIOStreamingHandler(BaseCallbackHandler):
    def __init__(self, sid):
        self.sid = sid

    async def emit(self, event, data):
        await sio.emit(event, data, room=self.sid)

    async def on_llm_new_token(self, token: str, **kwargs):
        await sio.emit("token", {"resposta": token}, room=self.sid)

# Conexão inicial
@sio.on('connect')
async def connect(sid, environ):
    print(f"Cliente conectado: {sid}")

# Função principal que roda o processamento
async def executar_tool(sid, user_message, arquivos):
    print(f"message: {user_message}")
    print(f"arquivos: {str(arquivos)}")
    config = {
        "configurable": {"thread_id": sid},
        "callbacks": [SocketIOStreamingHandler(sid=sid)],
        "streaming": True
    }

    inputs = {
        "messages": [HumanMessage(content=user_message)],
        "config": config
    }
    final_resposta = ""
    
    await sio.emit("status", {"resposta": "Iniciando..."}, room=sid)
    
    state = {"config": config}
    callbacks = state.get("config", {}).get("callbacks", []) or []
    for cb in callbacks:
        if hasattr(cb, 'emit'):
            await cb.emit("status", {"resposta": "Agente supervisor está pensando..."})
            break

    try:
        if arquivos and isinstance(arquivos, list):
            await sio.emit("analise", {"resposta": "\n\nLendo arquivos...\n\n"}, room=sid)

        async for chunk in system.astream(inputs, config=config, stream_mode="values"):
            msg = chunk["messages"][-1]
            print("Chunk recebido:", msg.content)
            final_resposta = msg.content

        resposta_final = final_resposta or "Desculpe, não consegui processar sua solicitação."
        await sio.emit("resposta_final", {"resposta": resposta_final}, room=sid)

    except Exception as e:
        await sio.emit("resposta_final", {"resposta": f"Erro: {str(e)}"}, room=sid)

# Escuta de mensagens do front-end
@sio.on('input_text')
async def handle_input(sid, data):
    print(data)
    user_message = data.get('input_data')
    arquivos = data.get('arquivos', [])
    asyncio.create_task(executar_tool(sid, user_message, arquivos))

# if __name__ == "__main__":
#     app.run(debug=True)