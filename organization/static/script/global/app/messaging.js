import { getCookies } from "../utils/cookie.js";
import { getAppName } from "./appName.js";

export async function sendMessage(url, body, method) {
    const messageSettings = {
        method: (method)?method:(body)?"POST":"GET",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": getCookies()["csrftoken"],
        },
        credentials: "include",
    };
    if (body) {
        messageSettings["body"] = JSON.stringify(body);
    }
    const app = getAppName();
    const result = await fetch(`/${app}${url}`, messageSettings);
    return result;
}

function validateValues(form) {
    const errors = form.validateValues();
    if (0 < errors.length) {
        for (const errorNum in errors) {
            const errorMessage = errors[errorNum];
            console.log(`Error ${errorNum}: ${errorMessage}`)
        }
        return errors;
    }
    return null;
}
export async function sendItemCreationMessage(form, itemType) {
    const errors = validateValues(form);
    if (errors) {
        return null;
    }
    const response = await sendMessage(`/new_item/?item_type=${itemType}`, form.getValues());
    return response;
}
export async function sendItemUpdateMessage(form, itemType, itemId) {
    const errors = validateValues(form);
    if (errors) {
        return null;
    }
    const response = await sendMessage(`/update_item/?item_type=${itemType}&item_id=${itemId}`, form.getValues(), "PATCH");
    return response;
} 