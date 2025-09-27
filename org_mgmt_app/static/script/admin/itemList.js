export class ItemList {
    constructor(itemType, updatedItemObtainer, onrefresh) {
        // An advanced dom item indexing system WILL NOT BE IMPLEMENTED because it takes too much time for this develop. For this development; lists will be completely refresh for each update.
        this.itemType = itemType;
        this.updatedItemObtainer = updatedItemObtainer;
        this.onrefresh = onrefresh;
    }
    async refresh(items) {
        if (!items) {
            items = await this.updatedItemObtainer();
        }
        await this.onrefresh(items);
    }
}