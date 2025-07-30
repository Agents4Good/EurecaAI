function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return decodeURIComponent(parts.pop().split(';').shift());
    return null;
}


async function deleteCookie(name) {
    document.cookie = `${name}=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;`;
    return;
}

async function store_token(name, value) {
    const date = new Date();
    date.setTime(date.getTime() + hoursExpiredIn * 60 * 60 * 1000);
    document.cookie = `${name}=${value};expires=${date.toUTCString()};path=/`;
}

function estaLogado() {
    const token = getCookie("profile");
    return !!token; // true se o token existir, false se não
}
