function formatCamelCase(str) {
    const exceptions = ['de', 'da', 'do', 'das', 'dos', 'e'];
    return str.toLowerCase().split(' ').map((word, index) => {
        if (exceptions.includes(word) && index !== 0) {
            return word;
        }
        return word.charAt(0).toUpperCase() + word.slice(1);
    }).join(' ');
}


async function get_resumo(texto) {
    try {
        const response = await fetch('/resumir', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ texto: texto })
        });

        if (!response.ok) { throw new Error('Erro na requisição: ' + response.status); }
        const data = await response.json();
        return data.resumo;
    } catch (erro) {
        console.error('Erro ao obter resumo:', erro);
        return null;
    }
}


function enable_input() {
    const textarea = document.getElementById('user_input');
    textarea.disabled = false;
    document.querySelector('.button_add_file').disabled = false;
}


function disable_input() {
    const textarea = document.getElementById('user_input');
    textarea.disabled = true;
    document.querySelector('.button_add_file').disabled = true;
}


function toggleMenu(id) {
    const menu = document.getElementById(`${id}_menu`);
    document.querySelectorAll('.fab-menu').forEach(m => {
        if (m !== menu) m.style.display = 'none';
    });

    if (menu) {
        menu.style.display = (menu.style.display === 'flex') ? 'none' : 'flex';
    }
}


async function fileToBase64(file) {
    return new Promise((resolve, reject) => {
        const reader = new FileReader();
        reader.onload = () => resolve(reader.result.split(',')[1]);
        reader.onerror = reject;
        reader.readAsDataURL(file);
    });
}

async function sendMessage(message) {
    render_ai_message();
    disable_input();
    scrollToBottom();
    scrollInUp = false;

    const $lastBotResponse = $('.bot__name__response').last();
    $lastBotResponse.text('');

    const pergunta_feita = document.getElementsByClassName("query");
    if (pergunta_feita.length > 0) {
        pergunta_feita[0].value = "";
        pergunta_feita[0].style.height = "30px";
    }

    const arquivosParaEnviar = [...arquivosSelecionados];
    reseta_arquivos('');

    const arquivosBase64 = await Promise.all(arquivosParaEnviar.map(async (file) => ({
        filename: file.name,
        content: await fileToBase64(file)
    })));

    socket.emit("input_text", {
        input_data: message,
        arquivos: arquivosBase64
    });

    socket.off("token");
    socket.off("resposta_final");
    socket.off("status");

    socket.on("status", (data) => {
        console.log(data.resposta)
        const $status = $lastBotResponse.closest('.bot').find('.bot__name__response_status');
        $status.text(data.resposta);
    });

    socket.on("token", (data) => {
        console.log(data)
        const $status = $lastBotResponse.closest('.bot').find('.bot__name__response_status');
        $status.text("");
        const span = document.createTextNode(data.resposta);
        $lastBotResponse[0].appendChild(span);
        $lastBotResponse.closest('.bot').removeClass('skeleton');
        //if (!scrollInUp) scrollToBottom();
    });

    socket.on("analise", (data) => {
        console.log("Mensagem analise recebida:", data.resposta);
    
        // Exemplo: mostrar a mensagem em um elemento da página
        const statusElement = document.querySelector('.bot__name__response_status');
        if (statusElement) {
            statusElement.textContent = data.resposta;
        }
    });

    socket.on("resposta_final", (data) => {
        $('.bot').last().find('.audio-button').show();
        const textoFinal = data.resposta;
        const htmlResponse = marked.parse(textoFinal);
        $lastBotResponse.html(htmlResponse);
        const cleanedResponse = textoFinal.trim().replace(/['"]/g, '');
        $('.audio-button').last().attr("onClick", `speak('${cleanedResponse}')`);
        $lastBotResponse.closest('.bot').removeClass('skeleton');

        const $status = $lastBotResponse.closest('.bot').find('.bot__name__response_status');
        $status.text("");

        if (!idChatLocal) {
            const newDiv = document.createElement("div");
            const id = `item_${Date.now()}`;
            newDiv.className = "history_item";
            newDiv.id = id;

            get_resumo(message).then((resumo) => {
                newDiv.innerHTML = `
                    <p style="white-space: nowrap; overflow: hidden; text-overflow: ellipsis;">${resumo}</p>
                    <div class="fab-wrapper">
                        <div class="fab" onclick="toggleMenu('${id}')"><i class='fas fa-ellipsis-h'></i></div>
                        <div class="fab-menu" id="${id}_menu">
                            <i class='fas fa-trash' onclick="apagar_chat('${id}')"></i>
                        </div>
                    </div>
                `;
                idChatLocal = id;
                document.getElementsByClassName("history")[0].appendChild(newDiv);
            });
        }

        scrollToBottom();
        enable_input();
    });
}
