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


function render_botao_historico(item) {
    const newDiv = document.createElement("div");
    newDiv.className = "history_item";
    newDiv.id = item.chat_id;
    newDiv.dataset.buttonId = item.chat_id;
    console.log(item.chat)
    newDiv.dataset.timestamp = item.timestamp;
    
    newDiv.onclick = function () {
        get_chat(item.chat_id);
        
        const todos = document.querySelectorAll('.history_item');
        todos.forEach(el => el.classList.remove('selecionado'));
    
        const elemento = document.querySelector(`.history_item#${item.chat_id}`);
        if (elemento) {
            elemento.classList.add('selecionado');
        }
    };
    
    newDiv.innerHTML = `
        <p style="white-space: nowrap; overflow: hidden; text-overflow: ellipsis;">${item.title}</p>
            <div class="fab-wrapper">
                <div class="fab" onclick="toggleMenu('${item.chat_id}')"><i class='fas fa-ellipsis-h'></i></div>
                <div class="fab-menu" id="${item.chat_id}_menu">
                    <i class='fas fa-trash' onclick="apagar_chat(${item.chat_id})"></i>
                </div>
            </div>
        `;
    
    document.getElementsByClassName("history")[0].appendChild(newDiv);
}


async function sendMessage(message, showStars) {
    const default_msg = "Os agentes podem levar até alguns minutos para pesquisar, analisar e responder. Exibiremos os resultados assim que os agentes tiverem processado os dados...  ";
    render_ai_message(default_msg, showStars);
    disable_input();
    scrollToBottom();
    scrollInUp = false;

    const $lastBotResponse = $('.bot__name__response').last();

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

    const profileStr = getCookie("profile");
    const res = profileStr ? JSON.parse(profileStr) : null;
    const perfil_response = res || {token: ""};
    const userToken = perfil_response && perfil_response["token"]

    console.log("CHAT ID QUE SERÁ ENVIADO: ", idChatLocal);
    socket.emit("input_text", {
        input_data: message,
        arquivos: arquivosBase64,
        token: userToken,
        chat_id: idChatLocal
    });

    socket.off("token");
    socket.off("resposta_final");
    socket.off("status");
    socket.off("agregando");
    socket.off("logos_sites");

    socket.on("logos_sites", (urls) => {
        const $bot = $lastBotResponse.closest('.bot');
        const $p = $bot.find('.bot__name p').first();
    
        const maxLogos = 3;
        const mostrar = urls.slice(0, maxLogos);
    
        const $logosContainer = $('<span class="logos-container"></span>');
    
        mostrar.forEach((url, i) => {
            const $img = $(`<img src="${url}" alt="Logo" class="bot__logo-img" style="opacity: 0; transition: opacity 0.3s ease;" />`);
            $logosContainer.append($img);
    
            setTimeout(() => {
                $img.css('opacity', 1);
            }, i * 400);
        });
    
        if (urls.length > maxLogos) {
            const $plus = $(`<span class="plus-icon" style="opacity: 0; transition: opacity 0.3s ease;">+</span>`);
            $logosContainer.append($plus);
    
            setTimeout(() => {
                $plus.css('opacity', 1);
            }, mostrar.length * 400);
        }
    
        $p.html('');
        $p.append($logosContainer);
        $p.append('<span class="assistente-text">Assistente:</span>');
    });            


    socket.on("status", (data) => {
        const $lastBot = $('.chat__container .bot').last();
        $lastBot.find('.bot__name__response_status').text(data.resposta);
    });

    socket.on("agregando", (data) => {
        const htmlResponse = marked.parse("");
        $lastBotResponse.html(htmlResponse);
    })

    socket.on("analise", (data) => {
        const statusElements = document.querySelectorAll('.bot__name__response_status');
        const statusElement = statusElements[statusElements.length - 1];

        if (statusElement) {
            statusElement.textContent = data.resposta;
        }
    });


    let streamingMarkdown = "";
    socket.on("token", (data) => {
        const token = data.resposta;
        streamingMarkdown += token;

        const html = marked.parse(streamingMarkdown);
        const $status = $lastBotResponse.closest('.bot').find('.bot__name__response_status');
        $status.text("");

        $lastBotResponse.html(html); // substitui com HTML convertido de Markdown
        $lastBotResponse.closest('.bot').removeClass('skeleton');
    });
    

    socket.on("resposta_final", (data) => {
        $('.bot').last().find('.audio-button').show();

        const textoFinal = data.resposta;
        const chat_id = data.chat_id;
        const htmlResponse = marked.parse(textoFinal);
        $lastBotResponse.html(htmlResponse);

        const cleanedResponse = textoFinal.trim().replace(/['"]/g, '');
        $('.audio-button').last().attr("onClick", `speak('${cleanedResponse}')`);

        $lastBotResponse.closest('.bot').removeClass('skeleton');
        const $status = $lastBotResponse.closest('.bot').find('.bot__name__response_status');
        $status.text("");

        // Verificar se chat_id já existe na lista de .history_item
        const historyContainer = document.querySelector('.history');
        const ids = [];

        if (historyContainer) {
            for (const filho of historyContainer.children) {
                if (filho.id) {
                    ids.push(filho.id);
                }
            }
        }

        // Se chat_id ainda não estiver no histórico
        console.log(ids, chat_id, idChatLocal)
        if (!idChatLocal || idChatLocal == null) {
            get_resumo(message)
                .then((resumo) => {
                    return fetch('/update_title', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({ chat_id, title: resumo })
                    }).then(() => resumo);
                })
                .then((resumo) => {
                    render_botao_historico({
                        title: resumo,
                        chat_id: chat_id,
                        timestamp: new Date().toISOString()
                    });
                });

        } else {
            // Se já existir, não adiciona novo botão e zera idChatLocal
            console.log("Chat já existe no histórico. Não adicionando.");
            idChatLocal = null;
        }

        // Atualiza timestamp se o item ainda for válido
        idChatLocal = chat_id;
        console.log(historyContainer, idChatLocal)
        const elemento = document.querySelector(`.history_item[data-button-id="${idChatLocal}"]`);
        console.log("Atualizando timestamp:", elemento);

        if (elemento) {
            elemento.dataset.timestamp = new Date().toISOString();
            ordenar_historico_por_data();
        }

        scrollToBottom();
        enable_input();
    });
}