window.onload = function() { 
    getProfile();

    const socket = io("http://127.0.0.1:8000", {
        transports: ['websocket']
    });
    
    socket.on("connect", () => {
        console.log("✅ Conectado ao servidor via Socket.IO!");

        const $lastBotResponse_get = $('.bot__name__response').last();
        const lastBotResponse_get = $lastBotResponse_get.get(0);
        const $responses_bots = $('.bot__name__response');
        console.log("Total de respostas de bots:", $responses_bots.length);

        if (lastBotResponse_get && lastBotResponse_get.dataset.ready !== "true" && $responses_bots.length > 1) {
            bot_alert_message("A conexão com o servidor foi restabelecida. Por favor, tente novamente!");
        }
    });

    socket.on("disconnect", () => {
        const $lastBotResponse_get = $('.bot__name__response').last();
        const lastBotResponse_get = $lastBotResponse_get.get(0);

        if (lastBotResponse_get && lastBotResponse_get.dataset.ready !== "true") {
            bot_alert_message("Ocorreu um erro! Você está desconectado do servidor.");
        }
    });
}


function bot_alert_message(mensagem) {
    console.log(mensagem);
    const $lastBotResponse = $('.bot__name__response').last();

    $('.bot').last().find('.audio-button').show();
    const textoFinal = mensagem;
    const htmlResponse = marked.parse(textoFinal);
    $lastBotResponse.html(htmlResponse);

    const cleanedResponse = textoFinal.trim().replace(/['"]/g, '');
    $('.audio-button').last().attr("onClick", `speak('${cleanedResponse}')`);

    $lastBotResponse.closest('.bot').removeClass('skeleton');
    const $status = $lastBotResponse.closest('.bot').find('.bot__name__response_status');
    $status.text("");

    const textarea = document.getElementById('user_input');
    textarea.disabled = false;
    document.querySelector('.button_add_file').disabled = false;

    enable_input();
    textarea.focus();
}


document.addEventListener("DOMContentLoaded", function () {
    const textarea = document.getElementById('user_input');
    function atualizarPlaceholder() {
        if (window.innerWidth < 600) {
            textarea.placeholder = "Digite sua dúvida sobre a UFCG...";
        } else {
            textarea.placeholder = "Pergunte informações sobre a UFCG...";
        }
    }

    atualizarPlaceholder();
    window.addEventListener('resize', atualizarPlaceholder);
    carregarHistorico();
});


async function carregarHistorico() {
    const profileStr = getCookie("profile");
    const res = profileStr ? JSON.parse(profileStr) : null;
    const perfil_response = res || {token: ""};
    const token = perfil_response && perfil_response["token"]
    
    if (perfil_response && token) {
        try {
            const response = await fetch("/get_historico", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({ token: token })
            });

            if (response.status === 200) {
                const data = await response.json();
                console.log(data)
                data
                .sort((a, b) => new Date(b.updated_at) - new Date(a.updated_at))
                .forEach(item => {
                    render_botao_historico(item);
                });
            } else {
                console.error("Erro na resposta:", response.status);
            }
        } catch (error) {
            console.error("Erro ao buscar histórico:", error);
        }
    }
}


function ordenar_historico_por_data() {
    const container = document.querySelector('.history');
    const botaoNovoChat = container.querySelector('.history_item.novo_chat');
    let itens = Array.from(container.querySelectorAll('.history_item:not(.novo_chat)'));

    //console.log(itens)

    itens.sort((a, b) => {
        const dataA = new Date(a.dataset.updated_at);
        const dataB = new Date(b.dataset.updated_at);
        return dataB - dataA;
    });

    // console.log(itens)

    container.innerHTML = '';

    if (botaoNovoChat) {
        container.appendChild(botaoNovoChat);
    }

    itens.forEach(item => {
        container.appendChild(item);
    });
}


$(document).ready(function () {
    $('#chat_form').on('keydown', function (event) {
        if (event.key === 'Enter') {
            if (event.shiftKey) {
                return;
            } else {
                event.preventDefault();
                var userMessage = $('#user_input').val();
                $('#user_input').val('');
                if (userMessage.trim() !== '') {
                    render_human_message(userMessage);
                    sendMessage(userMessage, true);
                }
            }
        }
    });
});



$(document).ready(function () {
    $('#chat_form').on('submit', function (event) {
        event.preventDefault();
        var userMessage = $('#user_input').val();
        $('#user_input').val('');
        if (userMessage.trim() !== '') {
            render_human_message(userMessage);
            sendMessage(userMessage, true);
        }
    });
});

document.addEventListener('DOMContentLoaded', function () {
    const form = document.getElementById('chat_form');
    if (form) {
        form.addEventListener('keypress', function(event) {
            if (event.key === 'Enter' && !event.shiftKey) {
                event.preventDefault();
                form.submit();
            }
        });
    }
});

const textarea = document.querySelector('.query');
const form = document.getElementById('chat_form');
if (form && textarea) {
    form.addEventListener('submit', function(event) {
        if (!textarea.value.trim()) {
            event.preventDefault();
        }
    });
}

function scrollToBottom() {
    $('.chat').animate({ scrollTop: $('.chat')[0].scrollHeight }, 200);
}

function openAsideBarMobile() {
    const aside = document.querySelector(".aside-chat");
    const buttonIcon = document.querySelector(".aside__mobile__button i");

    if (aside.classList.contains("open")) {
        aside.classList.remove("open");
        buttonIcon.classList.remove("fa-times");
        buttonIcon.classList.add("fa-bars");
    } else {
        aside.classList.add("open");
        buttonIcon.classList.remove("fa-bars");
        buttonIcon.classList.add("fa-times");
    }
}


function openMenu(id) {
    const menu = document.getElementById(id);
    const icon = menu.querySelector("i");
    const history = document.querySelector(".history");

    if (menu.classList.contains("open")) {
        menu.classList.remove("open");
        icon.classList.remove("fa-times");
        icon.classList.add("fa-ellipsis-h");
    } else {
        menu.classList.add("open");
        icon.classList.remove("fa-ellipsis-h");
        icon.classList.add("fa-times");
    }
}


function autoGrow(element) {
    element.style.height = "1px";
    const scrollHeight = element.scrollHeight;
    const maxHeight = 230;

    element.style.height = Math.min(scrollHeight, maxHeight) + "px";
}


function abrirSeletorArquivo() {
    const input = document.getElementById('fileInput');
    input.click();

    input.onchange = function () {
        const file = input.files[0];
        if (file) {
            arquivosSelecionados.push(file);

            const fileBox = document.createElement('div');
            fileBox.className = 'file-box';
            fileBox.textContent = file.name;

            const removeBtn = document.createElement('span');
            removeBtn.textContent = 'x';
            removeBtn.className = 'remove-file';
            removeBtn.onclick = function () {
                fileBox.remove();
                arquivosSelecionados = arquivosSelecionados.filter(f => f !== file);
            };

            fileBox.appendChild(removeBtn);
            const container = document.querySelector('.chat_aux_container_medium');
            container.appendChild(fileBox);

            input.value = '';
        }
    };
}


function reseta_arquivos(id) {
    arquivosSelecionados = [];
    document.querySelector('.chat_aux_container_medium').innerHTML = '';
    document.getElementById('user_input').value = '';
}


function addUserMessage(message) {
    let arquivosHTML = '';
    if (arquivosSelecionados.length > 0) {
        arquivosHTML = '<p class="mensagem_anexos">Arquivos anexados junto a mensagem:</p><div class="arquivos-enviados" style="margin-top: 10px; display: flex; flex-wrap: wrap; gap: 6px;">';
            arquivosSelecionados.forEach(file => {
            arquivosHTML += `<span class="arquivo-caixinha" style="background-color: #e0f0ff; color: #003366; padding: 4px 8px; border-radius: 12px; font-size: 12px; white-space: nowrap;">${file.name}</span>`;
        });
        arquivosHTML += '</div>';
    }

    const userMessageBlock = `
        <div class="user">
            <div class="user__name">
                <p>Você:</p>
            </div>
            <p class="user__response">${message}</p>
            ${arquivosHTML}
        </div>`;

    $('.chat__container').append(userMessageBlock);
    scrollToBottom();
}


function apagar_chat(id) {
    const isIdVazio = id === '';

    function apagar_chat_pelo_id(chatId) {
        console.log("apagando pelo id", chatId, idChatLocal);

        const historyItem = document.getElementById(chatId);
        const ehItemDeHistorico = historyItem && historyItem.classList.contains("history_item");
        const isChatSendoApagadoOAtual = chatId === idChatLocal;

        if (ehItemDeHistorico || chatId === '') {
            try {
                if (isChatSendoApagadoOAtual || chatId === '') {
                    document.querySelector('.chat__container').innerHTML = '';
                    document.querySelectorAll('.history_item').forEach(el => el.classList.remove('selecionado'));
                    idChatLocal = null;
                } else {
                    const historyItem = document.querySelector(`.history_item[data-button-id="${chatId}"]`);
                    historyItem?.classList.remove('selecionado');
                }
                historyItem?.remove();
            } catch (e) {
                console.error("Erro ao apagar chat pelo ID:", e);
            }
        }

        reseta_arquivos(chatId);
    }

    if (isIdVazio) {
        apagar_chat_pelo_id('');
    } else {
        $.ajax({
            type: 'POST',
            url: '/delete_chat',
            contentType: 'application/json',
            data: JSON.stringify({ chat_id: id }),
            timeout: 400000,
            success: function (_response, _textStatus, xhr) {
                const statusCode = xhr.status;
                console.log("Status HTTP:", statusCode);

                if (statusCode === 200) {
                    apagar_chat_pelo_id(id);
                } else {
                    console.warn("Resposta inesperada ao deletar chat:", statusCode);
                }
            },
            error: function (xhr, _status, error) {
                console.error("Erro ao tentar deletar chat. Status HTTP:", xhr.status, "-", error);
            }
        });
    }
}


// Trocar matricula por id
function get_chat(id) {
    if (idChatLocal != id) {
        
        const profileStr = getCookie("profile");
        const res = profileStr ? JSON.parse(profileStr) : null;
        const perfil_response = res || {token: ""};
        const token_response = perfil_response && perfil_response["token"]

        $.ajax({
            type: 'POST',
            url: '/get_chat',
            contentType: 'application/json',
            data: JSON.stringify({ chat_id: id, token: token_response }),
            success: function (response) {
                document.querySelector('.chat__container').innerHTML = '';
                const data = response.data;
                idChatLocal = id;

                data.forEach(message => {
                    if (message.human_message) {
                        arquivosSelecionados = message.arquivos || [];
                        render_human_message(message.human_message);
                        arquivosSelecionados = []
                    } else if (message.ai_message) {
                        render_ai_message(message.ai_message, false);
                        $('.bot').last().find('.audio-button').show();
                        const textoFinal = message.ai_message;
                        const htmlResponse = marked.parse(textoFinal);
                        const $lastBotResponse = $('.bot__name__response').last();
                        $lastBotResponse.html(htmlResponse);
                        const cleanedResponse = textoFinal.trim().replace(/['"]/g, '');
                        $('.audio-button').last().attr("onClick", `speak('${cleanedResponse}')`);
                        $lastBotResponse.closest('.bot').removeClass('skeleton');

                        const $status = $lastBotResponse.closest('.bot').find('.bot__name__response_status');
                        $status.text("");
                    }
                });
            },
            error: function(error) {
                console.log('Erro ao obter o chat:', error);
            }
        });
    }
}

function closeAllMenus() {
    document.querySelectorAll('.fab-menu').forEach(m => m.style.display = 'none');
}

function algumMenuAberto() {
    return Array.from(document.querySelectorAll('.fab-menu'))
        .some(m => getComputedStyle(m).display === 'flex');
}

function fechar_toggles() {
    if (algumMenuAberto()) {
        closeAllMenus();
    }
}

function toggleMenu(id) {
    closeAllMenus();
    const menu = document.getElementById(`${id}_menu`);
    if (!menu) return;

    const isVisible = getComputedStyle(menu).display === 'flex';

    if (!isVisible) {
        menu.style.display = 'flex';
    }
}

document.addEventListener('click', function (event) {
    setTimeout(() => {
        const isClickInsideFab = event.target.closest('.fab');
        const isClickInsideMenu = event.target.closest('.fab-menu');
    
        if (!isClickInsideFab && !isClickInsideMenu) {
            closeAllMenus();
        }
    }, 100);
});

function render_botao_historico(item) {
    const newDiv = document.createElement("div");
    newDiv.className = "history_item";
    newDiv.id = item.chat_id;
    newDiv.dataset.buttonId = item.chat_id;
    newDiv.dataset.updated_at = item.updated_at;

    newDiv.onclick = function () {
        get_chat(item.chat_id);
        
        // Tirando a cor em destaque de todos os botões do histórico.
        const todos = document.querySelectorAll('.history_item');
        todos.forEach(el => el.classList.remove('selecionado'));
    
        // Dando a cor em destaque apenas para o botão clicado.
        const elemento = document.querySelector(`.history_item[id="${item.chat_id}"]`);
        if (elemento) {
            elemento.classList.add('selecionado');
        }
    };
    
    newDiv.innerHTML = `
        <p style="white-space: nowrap; overflow: hidden; text-overflow: ellipsis;">${item.title}</p>
            <div class="fab-wrapper">
                <div class="fab">
                    <i class='fas fa-ellipsis-h'></i>
                </div>
                <div class="fab-menu" id="${item.chat_id}_menu" style="display: none;">
                    <i class='fas fa-trash'></i>
                </div>
            </div>
        `;
    
    document.getElementsByClassName("history")[0].appendChild(newDiv);

    const fab = newDiv.querySelector('.fab');
    const trashIcon = newDiv.querySelector('.fab-menu .fa-trash');

    fab.addEventListener('click', (e) => {
        e.stopPropagation();
        toggleMenu(item.chat_id);
    });

    trashIcon.addEventListener('click', (e) => {
        e.stopPropagation();
        apagar_chat(item.chat_id);
    });
}
