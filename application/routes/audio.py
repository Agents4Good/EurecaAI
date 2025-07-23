import speech_recognition as sr

from quart import Blueprint, request, jsonify
from io import BytesIO
from pydub import AudioSegment

bp = Blueprint("audio", __name__)

@bp.route("/voice-to-text", methods=["POST"])
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