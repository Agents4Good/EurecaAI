from flask import Flask, request, render_template, jsonify
from src.agents.build_graph import build
import speech_recognition as sr
from pydub import AudioSegment
from io import BytesIO

from langchain_core.messages import HumanMessage
import asyncio

from src.guardrails.validate_input import validate

app = Flask(__name__)

# Inicializa o sistema de agentes ao iniciar o aplicativo
system = build()

async def process_query(query):
    """
    Processa a consulta do usuário usando o sistema de agentes.
    """
    config = {"configurable": {"thread_id": None}}
    inputs = {"messages": [HumanMessage(content=validate(query))]}
    response = []

    async for chunk in system.astream(inputs, config, stream_mode="values"):
        chunk["messages"][-1].pretty_print()
        response.append(chunk["messages"][-1].content)
    return response[-1] if response else "Desculpe, não consegui processar sua solicitação."

@app.route('/')
def home():
    # Renderiza a página HTML onde o chatbot será exibido
    return render_template('index.html')

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