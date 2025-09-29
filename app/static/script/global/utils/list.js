export class List {
    constructor(value) {
        this.value = value;
    }
    get() {
        return this.value;
    }
    getElement(elementIdentifier) {
        return this.get()[elementIdentifier];
    }
    getLength() {
        return this.get().length;
    }
}