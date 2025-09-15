import { getById   } from './global/utils/dom/dom.js'
import { redirectToOriginalWebsite } from './global/redirect.js';
import { sendMessage } from './global/app/messaging.js';

async function sendLogInMessage() {
    const username = getById('username_input').value,
        password = getById('password_input').value;
    return await sendMessage('/login/', {username,password});
}
function showLoginError(response) {
    let errorText = null;
    const responseStatus = response.status;
    if (!responseStatus) {
        errorText = "Network error. Please check your connection and try again";
    } else if (responseStatus < 500) {
        errorText = "Login error";
    } else {
        errorText = "Login error. Please try again later";
    }
    getById("error_message").innerText = errorText;
}
async function sendLogInRequest() {
    const response = await sendLogInMessage();
    if (response.ok) {
        redirectToOriginalWebsite();
        return;
    }
    showLoginError(response);
}

getById("login_button").onclick = sendLogInRequest;