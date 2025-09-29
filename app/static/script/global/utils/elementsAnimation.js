export class ElementsAnimation {
    constructor(elementsListNodeId, elements, seoAltImgDescEnd) {
        this.nodeId = elementsListNodeId;
        this.elements = elements;
        this.seoAltImgDescEnd = ("" == seoAltImgDescEnd)?
            "" : " " + seoAltImgDescEnd;
    }
    getSeoAltImgDesc(element) {
        return element.getTitle() + this.seoAltImgDescEnd;
    }
}