import { getCookies } from "../utils/cookie.js";
import { getAppName } from "./appName.js";

export async function sendMessage(url, body, method) {
    const messageSettings = {
        method: (method)?method:"GET",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": getCookies()["csrftoken"],
        },
        credentials: "include",
    };
    if (body) {
        messageSettings["body"] = JSON.stringify(body);
    }
    const result = await fetch(`/${getAppName()}${url}`, messageSettings);
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
    const response = await sendMessage(`/item/`,
        {item_type:itemType, values:form.getValues()},
        "POST");
    return response;
}
export async function sendItemDeletionMessage(sectionInfo, itemId) {
    return await sendMessage(`/item/`,
        {item_type:sectionInfo["item_type"], id:itemId},
        "DELETE");
}
export async function sendItemUpdateMessage(form, itemType, itemId) {
    const errors = validateValues(form);
    if (errors) {
        return null;
    }
    const response = await sendMessage(`/item/`,
        {item_type:itemType, id:itemId, values:form.getValues()},
        "PATCH");
    return response;
} 