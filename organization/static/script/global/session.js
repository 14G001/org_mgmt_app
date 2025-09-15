import { getById } from "./utils/dom/dom.js";
import { redirect } from "./redirect.js";
import { getUrlResource, getUrlResourceAndQParams } from "./utils/url.js";
import { sendMessage } from "./app/messaging.js";

function logoutAllTabs() {
    const logout = localStorage.getItem("logout");
    if (!logout) {
        logout = "0";
    }
    localStorage.setItem("logout", parseInt(logout) + 1);
}
function logoutWindow() {
    if (getUrlResource(window).startsWith("/login/")) {
        return;
    }
    let nextUrl = getUrlResourceAndQParams(window);
    if (nextUrl === "/") {
        nextUrl = "";
    } else {
        nextUrl = `?next_url=${nextUrl}`;
    }
    redirect(`/login/${nextUrl}`);
}
async function sendLogoutMessage() {
    const response = await sendMessage('/logout/', null, "POST");
    if (response.ok) {
        logoutAllTabs();
        logoutWindow();
    }
    // @todo: Display error here
}

function initLogoutEventListener() {
    window.addEventListener("storage", event=>{
        if (event.key === "logout") {
            logoutWindow();
        }
    });
}
function initSessionEventListeners() {
    initLogoutEventListener();
}
function initSessionButtons() {
    // Function created to init the following buttons: login_button, logout_button and signin.
    const logoutButton = getById("logout_button")
    if (logoutButton) {
        logoutButton.onclick = sendLogoutMessage;
    }
}
export function initSessionElements() {
    initSessionEventListeners();
    initSessionButtons();
}