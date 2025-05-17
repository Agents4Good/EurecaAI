from flask import Flask, request, render_template, jsonify
import speech_recognition as sr
from pydub import AudioSegment
from io import BytesIO
from langchain_community.chat_models import ChatDeepInfra
from langchain_core.messages import HumanMessage
import asyncio, json

from demo.agents.eureca_chat import EurecaChat
from dotenv import load_dotenv

load_dotenv(override=True)

app = Flask(__name__)

# Inicializa o sistema de agentes ao iniciar a aplicação
system = EurecaChat(
    supervisor_model=ChatDeepInfra(model="meta-llama/Llama-3.3-70B-Instruct", temperature=0),
    aggregator_model=ChatDeepInfra(model="meta-llama/Llama-3.3-70B-Instruct", temperature=0, max_tokens=2048),
    agents_model=ChatDeepInfra(model="Qwen/Qwen3-14B", temperature=0, max_tokens=2048)
).build()

async def process_query(query):
    """
    Processa a consulta do usuário usando o sistema de agentes.
    """
    config = {"configurable": {"thread_id": "1"}}
    inputs = {"messages": [HumanMessage(content=query)]}
    response = []

    async for chunk in system.astream(inputs, config, stream_mode="values"):
        chunk["messages"][-1].pretty_print()
        response.append(chunk["messages"][-1].content)
    return response[-1] if response else "Desculpe, não consegui processar sua solicitação."

@app.route('/')
def home():
    # Renderiza a página HTML onde o chatbot será exibido
    return render_template('index.html')

@app.route('/login')
def login():
    # Renderiza a página HTML onde o login será exibido
    return render_template('login.html')

@app.route('/politica_termos')
def politica_termos():
    # Renderiza a página HTML onde o login será exibido
    return render_template('politica_termos.html')

@app.route('/delete_chat', methods=["POST"])
def delete_chat():
    return jsonify({"msg": "apagado"}), 200

@app.route('/resumir', methods=["POST"])
def resumir():
    data = request.get_json()

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
def chat():
    # Recebe a mensagem do usuário
    user_message = request.form['user_input']
    
    # Gera a resposta usando o sistema de agentes
    try:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        bot_message = loop.run_until_complete(process_query(user_message))
    except Exception as e:
        print(f"Erro ao processar a mensagem: {e}")
        bot_message = "Desculpe, ocorreu um erro ao processar sua solicitação."
    return {'response': bot_message}

@app.route("/voice-to-text", methods=["POST"])
def voice_to_text():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    
    audio_file = request.files['file']

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

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
