import { sendMessage } from "../global/app/messaging.js";
import { createElement, createText } from "../global/utils/dom/dom.js";
import { createWindow } from "./window.js";

export function getItemRemoveButtonAction(sectionInfo, itemId, itemStr, itemListToRefresh) {
    return async (event)=>{
        event.stopPropagation(); // Required to avoid keep pressing button container elements.
        const confirmationWindowInfo = createWindow("confirmation_window");
        const confirmationWindow = confirmationWindowInfo.element;
        const messageContainer = createElement(confirmationWindow, "div");
        createText(messageContainer, "p", `Desea eliminar ${sectionInfo["title"]["singular"].toLowerCase()}?`);
        const itemDataContainer = createElement(confirmationWindow, "div");
        createText(itemDataContainer, "p", itemStr);
        const optionButtonsContainer = createElement(confirmationWindow, "div", "confirmation_window_option_buttons_container");
        const confirmButton = createElement(optionButtonsContainer, "button");
        createText(confirmButton, "p", "Eliminar");
        confirmButton.onclick = async ()=>{
            const response = await sendMessage(`/delete_item/?item_type=${sectionInfo["item_type"]}&item_id=${itemId}`, null, "DELETE");
            if (response.ok) {
                itemListToRefresh.refresh();
            }
            confirmationWindowInfo.close();
        };
        const rejectButton = createElement(optionButtonsContainer, "button");
        createText(rejectButton, "p", "Cancelar");
        rejectButton.onclick = ()=>{
            confirmationWindowInfo.close();
        };
    };
}