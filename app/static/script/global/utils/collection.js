export function isIn(element, array) {
    const coincidence = array.find(item => {
        if (element == item) {
            return true;
        }
        return false;
    });
    return coincidence != undefined;
}