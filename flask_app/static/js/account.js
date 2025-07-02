function login_account() {
    const botaologin = document.querySelector(".login__button");
    const botaologinMobile = document.querySelector(".login_button_mobile");
    const word = botaologin.querySelector("span");
    const wordMobile = botaologinMobile.querySelector("span");

    if (word.textContent === "Login" || wordMobile.textContent === "Login") {
        window.location.href = '/login';
    } else if (word.textContent === "Sair" || wordMobile.textContent === "Sair" ) {
        deleteCookie("profile").then(() => {
            word.textContent = "Login";
            wordMobile.textContent = "Login";
            window.location.href = "/";
        });
    }
}


function getProfile() {
    const profileStr = getCookie("profile");
    const res = profileStr ? JSON.parse(profileStr) : null;
    
    if (res) {
        const username_ = formatCamelCase(res.name);
        const buttonText = document.querySelector(".login__button span");
        const buttonTextMobile = document.querySelector(".login_button_mobile span");

        if (buttonTextMobile || buttonText) {
            buttonTextMobile.textContent = "Sair";
            buttonText.textContent = "Sair";
        }

        const container = document.getElementsByClassName('chat__container')[0]; 
        const audioImgUrl   = container.getAttribute('data-audio-img');
        const botImgUrl   = container.getAttribute('data-bot-img');

        var botMessageBlock = `
            <div class="bot">
                <div class="bot__container">
                    <img src="${botImgUrl}" alt="" class="bot__img">
                    <div class="bot__response">
                        <div class="bot__name">
                            <p>Assistente:</p>
                        </div>
                        <p class="bot__name__response">Bem vindo de volta, ${username_}!\nA partir de agora, irei te chamar de ${username_.split(" ")[0]}.</p>
                        <div class="bot_options">
                            <button class="audio-button">
                                <img src="${audioImgUrl}" />
                            </button>
                        </div>  
                    </div>
                </div>
            </div>`;
        $('.chat__container').append(botMessageBlock);
    }
}