function speak(msg) {
    let synth = window.speechSynthesis;
    
    if (isSpeaking) {
        synth.cancel();
        isSpeaking = false;
    } else {
        const utterance = new SpeechSynthesisUtterance(msg);
        utterance.lang = 'pt-BR';
        utterance.pitch = 1;
        utterance.rate = 1;        
        const voices = synth.getVoices();
        utterance.voice = voices.find(voice => voice.lang === 'pt-BR') || voices[0];
        synth.speak(utterance);
        isSpeaking = true;
    }
}


function startRecording() {
    navigator.mediaDevices.getUserMedia({ audio: true })
    .then(stream => {
        mediaRecorder = new MediaRecorder(stream);
        mediaRecorder.start();

        mediaRecorder.ondataavailable = event => {
            audioChunks.push(event.data);
        };

        mediaRecorder.onstop = () => {
            const audioBlob = new Blob(audioChunks, { type: 'audio/wav' });
            const audioUrl = URL.createObjectURL(audioBlob);
            const audio = new Audio(audioUrl);
            audio.play(); 
            audioChunks = []; 
        };
    });
}


function stopRecording() {
    if (mediaRecorder) {
        mediaRecorder.stop();

        mediaRecorder.onstop = () => {
            const audioBlob = new Blob(audioChunks, { type: 'audio/wav' });
            audioChunks = [];

            const formData = new FormData();
            formData.append('file', audioBlob, 'recording.wav');

            $.ajax({
                type: 'POST',
                url: '/voice-to-text',
                data: formData,
                processData: false,
                contentType: false,
                success: function (data) {
                    const transcription = data.transcription;
                    if (transcription) {
                        render_human_message(transcription);
                        sendMessage(transcription);
                    }
                },
                error: function () {
                    console.error("Erro ao enviar o áudio:", error);
                }
            });
        };
    }
}


function changeImage(button) {
    const img = button.querySelector('img');
    const inputQuery = document.getElementsByClassName('query')[0]; 

    const micImg = button.getAttribute('data-mic-img');
    const audioImg = button.getAttribute('data-audio-img');

    if (img.src.includes('microphone.png')) {
        img.src = audioImg;
        img.style.backgroundColor = "#30ABED";
        inputQuery.disabled = true;
        inputQuery.style.backgroundColor = "white";
        startRecording();
    } else {
        img.src = micImg;
        img.style.backgroundColor = "#a6d1e9";
        inputQuery.disabled = false; 
        stopRecording();
    }
}