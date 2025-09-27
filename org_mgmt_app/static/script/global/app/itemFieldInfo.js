import { CommonFormInput, RelatedItemFormInput } from "../../admin/form.js";
import { ITM_MGMT_WIN_TYPE_VIEW_ITM } from "../../admin/manageItem.js";
import { createElement, createSectionToggleButton, createText, getByPosition } from "../utils/dom/dom.js";
import { getItemsInfo } from "./itemsInfo.js";
import { ITEM_TYPE_X_DOM_ELM_TYPE } from "./itemTypes.js";
import { sendMessage } from "./messaging.js";

export const FIELD_PARAM_IS_REQ = 0,
    FIELD_PARAM_TYPE     = 1,
    FIELD_PARAM_TITLE    = 2,
    FIELD_PARAM_EXTRA_INFO = 3;

async function createFormSection(parent, buttonMessage, formContentInitializer, className) {
    const formSectionContainer = createElement(parent, "div",`${className}_container`);

    const formSectionOptionButtons = createElement(formSectionContainer, "div",`${className}_buttons_container`);
    const formSectionToggleButton = createElement(formSectionOptionButtons, "button",`${className}_button`);
    const sectionToggleButtonArrow = createText(formSectionToggleButton, "p", "/\\"); // TODO: Check why some arrows are not working
    createText(formSectionToggleButton, "p", buttonMessage);
    const switchableSections = await formContentInitializer(formSectionContainer);

    createSectionToggleButton(formSectionToggleButton, switchableSections, sectionToggleButtonArrow, false);
    return formSectionContainer;
}

class SingleChoiceItemListTableBuilder {
    constructor() {}
    addFirstTheadParts(itemListTheadTr) {}
    addFirstItemPart(itemListTbodyTr) {}
    getOnClick(selectedItem, removeSelectedItemButton, firstItemPart, itemInfoStr, itemId) {
        return ()=>{
            selectedItem.innerText = itemInfoStr;
            selectedItem.dataset.id = itemId;
            removeSelectedItemButton.style.display = "block";
        };
    }
}

export class ItemFieldInfo {
    constructor(itemType, name, settings) {
        this.itemType   = itemType;
        this.name       = name;
        this.isRequired = settings[FIELD_PARAM_IS_REQ];
        this.type       = settings[FIELD_PARAM_TYPE];
        this.title      = settings[FIELD_PARAM_TITLE];
        this.extraInfo  = settings[FIELD_PARAM_EXTRA_INFO];
        if (!this.extraInfo) {
            this.extraInfo = {};
        }
    }
    log() {
        return `${this.name} = [Required:${this.isRequired} - Type:'${this.type}' - Title:'${this.title}']`;
    }
    getInputMessage(itemWindowType) {
        const isRequired = (this.isRequired && itemWindowType !== ITM_MGMT_WIN_TYPE_VIEW_ITM);
        return `${this.title}${isRequired?"*":""}:`
    }
    createCommonInput(inputContainer, inputType, commonValueClassName, defaultVal) {
        const input = inputType.getNewInput(30);
        input.className = commonValueClassName;
        if (defaultVal) {
            input.value = defaultVal;
        }
        inputContainer.appendChild(input);
        return new CommonFormInput(this, input);
    }
    resetSelectedItem(selectedItem, removeSelectedItemButton) {
        selectedItem.innerText = `None selected`;
        delete selectedItem.dataset.id;
        removeSelectedItemButton.style.display = "none";
    }
    addItemListTable(mainFormSectionContainer, selectedItem, removeSelectedItemButton,
        itemTypeInfo, itemList, relItemValueClassName, defaultVal) {
        const listItemInputBuilder = new SingleChoiceItemListTableBuilder();
        const itemListTable  = createElement(mainFormSectionContainer, "table", `${relItemValueClassName}_item_list`);
        const itemListThead  = createElement(itemListTable, "thead");
        const itemListTheadTr= createElement(itemListThead, "tr");
        listItemInputBuilder.addFirstTheadParts(itemListTheadTr);
        const listItemFields = itemTypeInfo["list_item_fields"];
        const itemTypeFields = itemTypeInfo["fields"];
        for (const fieldNumber in listItemFields) {
            const itemFieldName = listItemFields[fieldNumber];
            const itemListTheadTrTh = createElement(itemListTheadTr, "th");
            const fieldTitle = ("id" === itemFieldName)? "ID" :
                itemTypeFields[itemFieldName][FIELD_PARAM_TITLE];
            createText(itemListTheadTrTh, "div", fieldTitle);
        }
        const fieldsExtraInfo = {};
        for (const field in itemTypeFields) {
            fieldsExtraInfo[field] = itemTypeFields[field][FIELD_PARAM_EXTRA_INFO];
        }
        const itemListTbody = createElement(itemListTable, "tbody");
        for (const itemNum in itemList) {
            const item = itemList[itemNum];
            const itemId = item["id"];
            const itemFields = item["fields"];
            console.log(`ITEM ${itemId}`)
            console.log(JSON.stringify(item, null, 2))
            const itemListTbodyTr = createElement(itemListTbody, "tr", `${relItemValueClassName}_item_list_item`);
            itemListTbodyTr.dataset.id = itemId;
            const firstItemPart = listItemInputBuilder.addFirstItemPart(itemListTbodyTr, relItemValueClassName);
            const fieldValues = [];
            for (const fieldNumber in itemFields) {
                const fieldName = listItemFields[fieldNumber];
                let   fieldValue = itemFields[fieldNumber];
                const itemListTbodyTrTd = createElement(itemListTbodyTr, "td");
                const itemFieldContainer = createElement(itemListTbodyTrTd, "div", `${relItemValueClassName}_item_list_field_value`);
                if (fieldValue) {
                    fieldValues.push(fieldValue);
                } else {
                    const fieldTypeExtraInfo = fieldsExtraInfo[fieldName];
                    let nullVal = fieldTypeExtraInfo?.null_case;
                    if (!nullVal) {
                        nullVal = "-";
                    } 
                    fieldValue = nullVal;
                }
                createText(itemFieldContainer, "p", fieldValue);
            }
            itemListTbodyTr.onclick = listItemInputBuilder.getOnClick(
                selectedItem, removeSelectedItemButton, firstItemPart, fieldValues.join(" - "), itemId);
            if (defaultVal && itemId === defaultVal) {
                itemListTbodyTr.click();
            }
        }
        return itemListTable;
    }
    async createRelatedItemSelectInput(inputContainer, relItemValueClassName, defaultVal) {
        inputContainer.className = `${relItemValueClassName}_container`;
        let itemListInfo = await sendMessage(`/items_section?item_type=${this.type}`);
        itemListInfo = await itemListInfo.json();
        itemListInfo = itemListInfo["section"];
        const itemsInfo = await getItemsInfo();
        const mainFormContentInitializer = async (mainFormSectionContainer)=>{
            const mainFormSectionOptions = getByPosition(mainFormSectionContainer, [0]);
            const formSectionToggleButton = getByPosition(mainFormSectionOptions, [0]);
            const selectedItem = createElement(formSectionToggleButton, "button", `${relItemValueClassName}_selected`);
            const removeSelectedItemButton = createElement(formSectionToggleButton, "button", `${relItemValueClassName}_remove_selected_item_button`);
            createText(removeSelectedItemButton, "p", "X");
            this.resetSelectedItem(selectedItem, removeSelectedItemButton);
            removeSelectedItemButton.onclick = (event)=>{
                this.resetSelectedItem(selectedItem, removeSelectedItemButton);
                event.stopPropagation();
            };
            const itemListTable = this.addItemListTable(
                mainFormSectionContainer, selectedItem, removeSelectedItemButton,
                itemsInfo[this.type], itemListInfo["items"], relItemValueClassName,
                defaultVal);
            return [itemListTable];
        };
        const inputSection = await createFormSection(inputContainer, this.getInputMessage(), mainFormContentInitializer, relItemValueClassName);
        const input =  getByPosition(inputSection, [0,0,2]);
        return new RelatedItemFormInput(this, input);
    }
    async createFieldElement(parent, itemTypesInfo, classNames, defaultVal, itemMgmtWindowInfo) {
        const commonValueClassName = classNames[0],
            relItemValueClassName = classNames[1];
        const itemWindowType = itemMgmtWindowInfo.type;
        const inputContainer = createElement(parent, "div");
        const inputType = ITEM_TYPE_X_DOM_ELM_TYPE[this.type];
        if (inputType || itemWindowType === ITM_MGMT_WIN_TYPE_VIEW_ITM) {
            inputContainer.className = `${commonValueClassName}_container`;
            createText(inputContainer, "p", this.getInputMessage(itemWindowType));
            if (itemWindowType === ITM_MGMT_WIN_TYPE_VIEW_ITM) {
                if (!defaultVal) {
                    defaultVal = itemTypesInfo[this.itemType]["fields"][this.name][FIELD_PARAM_EXTRA_INFO];
                    defaultVal = defaultVal?.null_case || "-";
                }
                createText(inputContainer, "p", defaultVal);
                return null;
            }
            return this.createCommonInput(
                inputContainer, inputType, commonValueClassName, defaultVal, itemMgmtWindowInfo);
        }
        const itemTypeInfo = itemTypesInfo[this.type];
        if (itemTypeInfo) {
            return await this.createRelatedItemSelectInput(
                inputContainer, relItemValueClassName, defaultVal);
        }
        throw `Error at ItemFieldInfo.createFieldElement: this.type has a not supported value: ${this.type}`;
        return null;
    }
}