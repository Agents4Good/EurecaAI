function render_human_message(message) {
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


function render_ai_message(message, showStars) { 
    const container = document.getElementsByClassName('chat__container')[0]; 
    const audioImgUrl   = container.getAttribute('data-audio-img');
    const botImgUrl     = container.getAttribute('data-bot-img');
    const brilhosImgUrl = container.getAttribute('data-brilhos-gif');

    var botMessageBlock = `
        <div class="bot skeleton">
            <div class="bot__container">
                <img src="${botImgUrl}" alt="" class="bot__img">
                <div class="bot__response">
                    <div class="bot__name">
                        <p>Assistente:</p>
                        <p class="bot__name__response_status"></p>
                    </div>
                    <p class="bot__name__response">
                        ${message}
                        ${showStars ? `<img src="${brilhosImgUrl}" alt="✨" style="width: 20px; height: 20px; vertical-align: middle; margin-left: 4px;">` : ""}
                    </p>                    
                    <div class="bot_options">
                        <button class="audio-button" style="display: none;">
                            <img src="${audioImgUrl}" />
                        </button>
                    </div>
                </div>
            </div>
        </div>`;
    $('.chat__container').append(botMessageBlock);
}
