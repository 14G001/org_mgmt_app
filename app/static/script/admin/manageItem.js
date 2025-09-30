import { ItemFieldInfo } from "../global/app/itemFieldInfo.js";
import { getItemsInfo } from "../global/app/itemsInfo.js";
import { sendItemCreationMessage, sendItemUpdateMessage, sendMessage } from "../global/app/messaging.js";
import { createElement, createText } from "../global/utils/dom/dom.js";
import { Form } from "./form.js";
import { createWindow } from "./window.js";

export const ITM_MGMT_WIN_TYPE_NEW_ITM = 0,
    ITM_MGMT_WIN_TYPE_EDIT_ITM = 1,
    ITM_MGMT_WIN_TYPE_VIEW_ITM = 2;

export class ItemManagementWindow {
    constructor(type, itemId, className) {
        this.type = type; // new/edit/view
        this.itemId = itemId;
        this.className = className;
    }
}

async function initItemManagementWindow(itemWindowInfo, itemTypesInfo, itemType, itemListToRefresh, itemMgmtWindowInfo, classNames) {
    const itemWindow = itemWindowInfo.element;
    const itemTypeInfo = itemTypesInfo[itemType];
    const isItemViewWindowType = (itemMgmtWindowInfo.type === ITM_MGMT_WIN_TYPE_VIEW_ITM);
    if (isItemViewWindowType) {
        const exitButton = createElement(itemWindow, "div", `${itemMgmtWindowInfo.className}_close_button`);
        createText(exitButton, "p", "X");
        exitButton.onclick = ()=>{
            itemWindowInfo.close();
        };
        createText(itemWindow, "div", itemTypeInfo["title"]["singular"], `${itemMgmtWindowInfo.className}_title`);
    }
    const form = new Form();
    const itemId = itemMgmtWindowInfo.itemId;
    let fields = itemTypeInfo["fields"];
    if (!fields) {
        fields = itemTypesInfo[itemTypeInfo["source"]["type"]]["fields"];
    }
    const itemWindowInputs = createElement(itemWindow, "div", "update_item_window_form_inputs");
    let defaultValues = null;
    if (itemId) {
        const valueTypes = (isItemViewWindowType)? "info" : "value";
        const response = await sendMessage(
            `/item/?item_type=${itemType}&id=${itemId}&value_types=${valueTypes}`);
        const responseJson = await response.json();
        defaultValues = responseJson["item_fields"];
        if (isItemViewWindowType) {
            defaultValues = defaultValues[0]["fields"];
        }
    }
    let fieldNum = 0;
    for (const field in fields) {
        const fieldInfo = new ItemFieldInfo(itemType, field, fields[field]);
        let defaultVal = defaultValues;
        if (defaultValues) {
            defaultVal = (isItemViewWindowType)?
                defaultValues[fieldNum] :
                defaultVal[fieldInfo.name];
        }
        const input = await fieldInfo.createFieldElement(itemWindowInputs,
            itemTypesInfo, classNames, defaultVal, itemMgmtWindowInfo);
        form.addInput(input);
        fieldNum++;
    }
    if (isItemViewWindowType) {
        return;
    }
    const submitButtonContainer = createElement(itemWindow, "div", "update_item_window_form_submit_container");
    const submitButton = createElement(submitButtonContainer, "button", "update_item_window_form_submit");
    createText(submitButton, "p", (defaultValues)?"Actualizar":"Crear");
    submitButton.onclick = async ()=>{
        if (defaultValues) {
            const result = await sendItemUpdateMessage(form, itemType, itemId);
            console.log(`update result: ${result}`)
        } else {
            const result = await sendItemCreationMessage(form, itemType);
            console.log(`creation result: ${result}`)
        }
        await itemListToRefresh.refresh();
        itemWindowInfo.close();
    };
}
export function getItemManagementButtonAction(itemType, itemListToRefresh, itemMgmtWindowInfo, classNames) {
    const windowClassName = itemMgmtWindowInfo.className || "window";
    if (!classNames) {
        classNames = ["input_value", "input_related_item"];
    }
    return async ()=>{
        const itemWindowInfo = createWindow(windowClassName);
        const itemsFieldInfo = await getItemsInfo();
        await initItemManagementWindow(
            itemWindowInfo, itemsFieldInfo, itemType, itemListToRefresh, itemMgmtWindowInfo, classNames);
    };
}