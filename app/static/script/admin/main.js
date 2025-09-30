import { sendMessage } from '../global/app/messaging.js';
import { createSectionToggleButton, getById, createText, createElement, removeElementChilds } from '../global/utils/dom/dom.js'
import { getGlobalVar } from '../global/utils/dom/dom.js';
import { ItemList } from './itemList.js';
import { getItemManagementButtonAction, ITM_MGMT_WIN_TYPE_VIEW_ITM, ITM_MGMT_WIN_TYPE_EDIT_ITM, ItemManagementWindow, ITM_MGMT_WIN_TYPE_NEW_ITM } from './manageItem.js';
import { getItemRemoveButtonAction } from './removeItem.js';
import { FIELD_PARAM_EXTRA_INFO } from '../global/app/itemFieldInfo.js';
import { getItemsInfo } from '../global/app/itemsInfo.js';

function initItemFields(itemTr, itemTypeFields, fieldTypes, itemFieldValues) {
    const itemFields = [];
    for (const itemFieldNum in itemFieldValues) {
        const fieldValueContainer = createElement(itemTr, "td");
        let fieldValue = itemFieldValues[itemFieldNum];
        if (!fieldValue) {
            let nullVal = itemTypeFields[fieldTypes[itemFieldNum]][FIELD_PARAM_EXTRA_INFO];
            if (nullVal) {
                nullVal = nullVal["null_case"];
            }
            if (!nullVal) {
                nullVal = "-";
            }
            fieldValue = nullVal;
        }
        createText(fieldValueContainer, "div", fieldValue, "org_elm_item_field_value");
        itemFields.push(fieldValueContainer);
        fieldValueContainer.onmouseenter = ()=>{
            const hoverColor = getGlobalVar("--item-info-bg-color-hover").slice(1, -1); // slice required to remove first and last '"' symbols. Required for rgb(a,b,c) values.
            for (const fieldNum in itemFields) {
                itemFields[fieldNum].style.background = hoverColor;
            }
        };
        fieldValueContainer.onmouseleave = ()=>{
            for (const fieldNum in itemFields) {
                itemFields[fieldNum].style.removeProperty("background-color");
            }
        }
    }
}
function initItemAvailableActions(sectionInfo, itemTr, itemListToRefresh, itemId, itemFieldValues) {
    const availableActions = sectionInfo["actions"];
    if ("" === availableActions) {
        return;
    }
    const itemOptionsContainer = createElement(itemTr, "td");
    const itemOptions = createElement(itemOptionsContainer, "div", "item_options");
    if (availableActions.includes("u")) {
        const itemEditButton = createElement(itemOptions, "button", "item_edit_button");
        createText(itemEditButton, "p", "Modificar");
        itemEditButton.onclick = async (event)=>{
            event.stopPropagation();
            await getItemManagementButtonAction(sectionInfo["item_type"], itemListToRefresh,
                new ItemManagementWindow(ITM_MGMT_WIN_TYPE_EDIT_ITM, itemId))();
        };
    }
    if (availableActions.includes("d")) {
        const itemRemoveButton = createElement(itemOptions, "button", "item_remove_button");
        createText(itemRemoveButton, "p", "Eliminar");
        const itemStrFields = [];
        for (const fieldNum in itemFieldValues) {
            const value = itemFieldValues[fieldNum];
            if (value) {
                itemStrFields.push(value);
            }
        }
        itemRemoveButton.onclick = getItemRemoveButtonAction(sectionInfo,
            itemId, itemStrFields.join(" - "), itemListToRefresh
        );
    }
}
async function initListItems(sectionInfo, tbody, items, itemListToRefresh) {
    const itemsInfo = await getItemsInfo();
    removeElementChilds(tbody);
    const itemType = sectionInfo["item_type"];
    const itemTypeInfo = itemsInfo[itemType];
    const fieldTypes = itemTypeInfo["list_item_fields"];
    const itemTypeFields = itemTypeInfo["fields"];
    for (const itemNum in items) {
        const item = items[itemNum];
        const itemId = item["id"];
        const itemTr = createElement(tbody, "tr");
        itemTr.onclick = getItemManagementButtonAction(itemType, itemListToRefresh,
            new ItemManagementWindow(ITM_MGMT_WIN_TYPE_VIEW_ITM, itemId, "item_view_window"), ["view_value", "view_related_item"]);
        const itemFieldValues = item["fields"];
        initItemFields(itemTr, itemTypeFields, fieldTypes, itemFieldValues);
        initItemAvailableActions(sectionInfo, itemTr, itemListToRefresh, itemId, itemFieldValues);
    }
}
async function initSectionItemList(itemList, sectionInfo) {
    const listItemType = sectionInfo["item_type"];
    const thead    = createElement(itemList, "thead", "org_elms_adm_items_fields_thead");
    const headTr   = createElement(thead, "tr");
    const fieldTitles = sectionInfo["field_titles"];
    for (const titleNum in fieldTitles) {
        const fieldTitle = fieldTitles[titleNum];
        const th = createElement(headTr, "th");
        createText(th, "div", fieldTitle);
    }
    const availableActions = sectionInfo["actions"];
    let newItemThButton = null;
    let addCreateButton = false;
    if ("" !== availableActions) {
        const newItemTh = createElement(headTr, "th");
        addCreateButton = availableActions.includes("c");
        if (addCreateButton) {
            newItemThButton = createElement(newItemTh, "button", "org_elms_adm_item_addition_button");
            createText(newItemThButton, "p", "Nuevo +");
        }
    }

    const tbody = createElement(itemList, "tbody");
    const itemListInfo = new ItemList(listItemType,
        async ()=>{
            const response = await sendMessage(`/items_section/?item_type=${listItemType}`);
            const responseJson = await response.json();
            console.log("RSP:")
            console.log(JSON.stringify(responseJson, null, 2))
            const items = responseJson["section"]["items"]
            return items;
        },
        async (items)=>{
            if ("" === availableActions) {
                console.log("Items")
                console.log(JSON.stringify(items, null, 2))
            }
            await initListItems(sectionInfo, tbody, items, itemListInfo);
        }
    );
    if (addCreateButton) {
        newItemThButton.onclick = getItemManagementButtonAction(
            listItemType, itemListInfo, new ItemManagementWindow(ITM_MGMT_WIN_TYPE_NEW_ITM));
    }
    await itemListInfo.refresh(sectionInfo["items"]);
}

async function init() {
    const response = await sendMessage(`/home_items/`);
    const sections = await response.json();
    console.log("HOME ITEMS")
    console.log(JSON.stringify(sections, null, 2))
    const sectionsInfo = sections["sections"];
    const sectionsContainer = getById("organization_elements");
    for (const sectionNum in sectionsInfo) {
        const sectionInfo = sectionsInfo[sectionNum];
        const AppElmSection = createElement(sectionsContainer, "section")
        const titleContainer = createElement(AppElmSection, "h2");
        const title = createElement(titleContainer, "div", "org_elm_admin_toggle_button");
        const arrow = createText(title, "div", "/\\");
        createText(title, "p", sectionInfo["title"]["plural"]);
        const itemList = createElement(AppElmSection, "table", "org_elms_adm_items");
        createSectionToggleButton(titleContainer, [itemList], arrow, false);
        await initSectionItemList(itemList, sectionInfo);
    }
}

init();