import { sendMessage } from "./messaging.js";

let itemsInfo = null;

export async function getItemsInfo() {
    if (!itemsInfo) {
        const response = await sendMessage('/items_info/');
        itemsInfo = await response.json();
    }
    return itemsInfo;
}