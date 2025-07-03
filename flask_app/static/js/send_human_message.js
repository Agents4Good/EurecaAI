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


function sendMessage(message) {
    render_ai_message();
    disable_input();
    const $lastBotResponse = $('.bot__name__response').last();
    const pergunta_feita = document.getElementsByClassName("query");
    if (pergunta_feita.length > 0) {
        pergunta_feita[0].value = "";
        pergunta_feita[0].style.height = "30px";
    }

    const arquivosParaEnviar = [...arquivosSelecionados];
    reseta_arquivos('');

    const formData = new FormData();
    formData.append('input_data', message);

    arquivosParaEnviar.forEach((file, i) => {
        formData.append('archives[]', file);
    });

    const profileStr = getCookie("profile");
    if (profileStr) {
        formData.append('profile', profileStr)
    }

    $.ajax({
        type: 'POST',
        url: '/chat',
        timeout: 120000,
        data: formData,
        processData: false,
        contentType: false,
        success: function (response) {
            const markdownResponse = response.response;
            const htmlResponse = marked.parse(markdownResponse);
            $('.bot').last().find('.audio-button').show();
            $lastBotResponse.html(htmlResponse);
            $lastBotResponse.closest('.bot').removeClass('skeleton');
            const cleanedResponse = (markdownResponse.trim()).replace(/['"]/g, '');
            $('.audio-button').last().attr("onClick", `speak('${cleanedResponse}')`);

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
        },
        error: function (jqXHR, textStatus, errorThrown) {
            if (textStatus === 'timeout') {
                $('.bot__name__response').last().text('Desculpe, o tempo de espera foi excedido.');
            } else {
                $('.bot__name__response').last().text('Desculpe, algo deu errado.');
            }
            $lastBotResponse.closest('.bot').removeClass('skeleton');
            enable_input();
        }
    });
}