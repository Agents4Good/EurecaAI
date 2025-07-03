function login_account() {
    const botaologin = document.querySelector(".login__button");
    const botaologinMobile = document.querySelector(".login_button_mobile");

    const word = botaologin ? botaologin.querySelector("span") : null;
    const wordMobile = botaologinMobile ? botaologinMobile.querySelector("span") : null;

    const textoDesktop = word?.textContent;
    const textoMobile = wordMobile?.textContent;

    if (textoDesktop === "Login" || textoMobile === "Login") {
        window.location.href = '/login';
    } 
    else if (textoDesktop === "Sair" || textoMobile === "Sair") {
        deleteCookie("profile").then(() => {
            if (word) word.textContent = "Login";
            if (wordMobile) wordMobile.textContent = "Login";
            window.location.href = "/";
        });
    }
}


function getProfile() {
    const profileStr = getCookie("profile");
    const res = profileStr ? JSON.parse(profileStr) : null;
    
    if (res && res.name) {
        const username_ = formatCamelCase(res.name);

        const buttonText = document.querySelector(".login__button span");
        const buttonTextMobile = document.querySelector(".login_button_mobile span");

        if (buttonText) buttonText.textContent = "Sair";
        if (buttonTextMobile) buttonTextMobile.textContent = "Sair";

        const container = document.querySelector('.chat__container'); 
        if (!container) return;

        const audioImgUrl = container.getAttribute('data-audio-img') || 'default-audio.png';
        const botImgUrl   = container.getAttribute('data-bot-img') || 'default-bot.png';
        const firstName = username_.split(" ")[0];

        const botMessageBlock = `
            <div class="bot">
                <div class="bot__container">
                    <img src="${botImgUrl}" alt="" class="bot__img">
                    <div class="bot__response">
                        <div class="bot__name">
                            <p>Assistente:</p>
                        </div>
                        <p class="bot__name__response">Bem-vindo de volta, ${username_}!<br>A partir de agora, irei te chamar de <strong>${firstName}</strong>.
                        </p>
                        <div class="bot_options">
                            <button class="audio-button">
                                <img src="${audioImgUrl}" />
                            </button>
                        </div>  
                    </div>
                </div>
            </div>`;

        container.insertAdjacentHTML("beforeend", botMessageBlock);
    }
}