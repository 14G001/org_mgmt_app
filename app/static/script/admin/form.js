export class Form {
    constructor() {
        this.inputs = [];
    }
    log() {
        console.log("Form:")
        console.log(JSON.stringify(this.getValues(), null, 2)) // Warning: JSON.stringify does not print on string fields with undefined value.
    }
    getValues() {
        const fields = {};
        for (const inputNum in this.inputs) {
            const input = this.inputs[inputNum];
            let value = input.getValue();
            if (!value) {
                value = null;
            }
            fields[input.fieldInfo.name] = value;
        }
        return fields;
    }
    validateValues() {
        const errors = [];
        for (const inputNum in this.inputs) {
            const validationResult = this.inputs[inputNum].validateValue();
            if (validationResult) {
                errors.push(validationResult);
            }
        }
        return errors;
    }
    addInput(input) {
        this.inputs.push(input);
    }
}

export class CommonFormInput {
    constructor(fieldInfo, input) {
        this.fieldInfo = fieldInfo;
        this.input = input;
    }
    log() {
        console.log(`INPUT> field: ${this.fieldInfo.name} - value: <${this.getValue()}>`);
    }
    validateValue() {
        const value = this.getValue();
        if (this.fieldInfo.isRequired && !value) {
            return `Error: ${this.fieldInfo.title} field must not be empty.`;
        }
        return null;
    }
    getValue() {
        return this.input.value;
    }
}
export class RelatedItemFormInput extends CommonFormInput {
    getValue() {
        return Number(this.input.dataset.id);
    }
}