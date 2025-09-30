import { createElement } from "../utils/dom/dom.js";

// TODO x 2: 1) Move from here? - 2) Test each input type - 3) Modularize adding a function "createFieldElement" or something like that.
class InputType {
    constructor(inputType) {
        this.inputType = inputType;
    }
    validateKeyDownEventChars(event, input) {
        return true;
    }
    onKeyDown(event, input, maxDigits) {
        const keyCode = event.keyCode;
        if (keyCode === 8 // Clear with backspace
            || keyCode === 37 || keyCode === 39) { // Move with arrows (<- and ->)
            return true;
        }
        if (maxDigits-1 < input.value.length) {
            return false;
        }
        return this.validateKeyDownEventChars(event, input);
    }
    getNewInput(maxDigits) {
        const input = createElement(null, "input");
        if (this.inputType) {
            input.type = this.inputType;
        }
        input.onkeydown = (event)=>{
            return this.onKeyDown(event, input, maxDigits);
        }
        return input;
    }
}
class IntegerInputType extends InputType {
    validateKeyDownEventChars(event, input) {
        const keyCode = event.key.charCodeAt(0);
        return (47 < keyCode && keyCode < 58);// Is number
    }
}
class FloatInputType extends IntegerInputType {
    validateKeyDownEventChars(event, input) {
        if (super.validateKeyDownEventChars(event, input)) {
            return true;
        }
        const value = input.value;
        const valueLen = value.length;
        for (let charNum = 0; charNum < valueLen; charNum++) {
            if ([44,46].includes(value.charCodeAt(charNum))) { // Previously had a dot or comma
                return false;
            }
        }
        const keyCode = event.key.charCodeAt(0);
        return [44,46].includes(keyCode); // Is a dot or comma
    }
}
class TextInputType extends InputType {
}
class DatetimeInputType extends InputType {
    onKeyDown(event, input, maxDigits) {
        return true;
    }
}

export const ITEM_TYPE_X_DOM_ELM_TYPE = {
    int  : new IntegerInputType    (),
    float: new FloatInputType      (),
    str  : new TextInputType       (),
    datetime: new DatetimeInputType("datetime-local"),
    date : new DatetimeInputType   ("date"),
    time : new DatetimeInputType   ("time")
};