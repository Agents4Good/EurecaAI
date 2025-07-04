window.onload = function() { 
    getProfile();

    const socket = io("http://127.0.0.1:8000", {
    transports: ['websocket']
    });
    
    socket.on("connect", () => {
      console.log("✅ Conectado ao servidor via Socket.IO!");
      console.log("ID do socket:", socket.id);
    });
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
});


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
                    sendMessage(userMessage);
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
            sendMessage(userMessage);
        }
    });
});


const form = document.getElementById('chat_form');
form.addEventListener('keypress', function(event) {
    if (event.keyCode === 13 && !event.shiftKey) {
        event.preventDefault();
        form.submit();
    }
});


const textarea = document.querySelector('.query');
form.addEventListener('submit', function(event) {
    if (!textarea.value.trim()) {
        event.preventDefault();
    }
});


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


// Ver
function apagar_chat(id) {
    function apagar_chat_pelo_id(id) {
        document.querySelector('.chat__container').innerHTML = '';
        const historyItem = document.getElementById(id);
        if ((historyItem && historyItem.classList.contains("history_item")) || id == '') {
            try {
                historyItem.remove();
            } catch {}
            if (id == idChatLocal || id == '') {
                idChatLocal = null;
            }
        }

        reseta_arquivos(id);
    }

    if (id == '') {
        apagar_chat_pelo_id('');
        reseta_arquivos('');
    } else {
        $.ajax({
            type: 'POST',
            url: '/delete_chat',
            timeout: 400000,
            success: function (response) {
                apagar_chat_pelo_id(id);
            }
        });
    }
}