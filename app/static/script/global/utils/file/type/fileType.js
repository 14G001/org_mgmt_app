import {createImg} from "../../dom/dom.js";

export class FileType {
    constructor(file) {
        this.file = file;
    }
    getNode(parent, className, seoAltImgDesc) {
        return createImg(parent, className, seoAltImgDesc, this.file.getFullPath());
    }
}