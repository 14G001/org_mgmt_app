import { createElement, createText, getById  } from './global/utils/dom/dom.js'
import { sendMessage } from './global/app/messaging.js';
import { redirectToOriginalWebsite } from './global/redirect.js';

async function init() {
    const result = await sendMessage('/test_users/');
    const items  = await result.json();
    console.log("RESPONSE")
    console.log(JSON.stringify(items, null, 2))
    const userListContainer = getById("user_list_container");
    const users = items["users"];
    for (const userNumber in users) {
        const userFields = users[userNumber]["fields"]
        const username = userFields[0];
        const userString = userFields.slice(1).join(" - ");
        const userButtonContainer = createElement(userListContainer, "div", "user_button_container");
        const userButton = createElement(userButtonContainer, "button", "user_button");
        userButton.onclick = async ()=>{
            await sendMessage('/test_login/', {username});
            redirectToOriginalWebsite();
        };
        createText(userButton, "p", userString, "user_button_text");
    }
}

await init()