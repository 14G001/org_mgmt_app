import {MediaContainer} from "./mediaContainer.js";
import {createImg, createTextTooltip} from "../dom/dom.js";

export class LogoContainer extends MediaContainer {
    constructor(logoFileName, tooltipText, url) {
        super(logoFileName, url);
        this.tooltipText = tooltipText;
    }
    setLogoFileName(logoFileName) {
        this.mediaFileName = logoFileName;
    }
    getLogoFileName() {
        return this.mediaFileName;
    }
    getTooltipText() {
        return this.tooltipText;
    }
    getLogoMediaPath() {
        throw new Error("Implement method MediaContainer.getLogoMediaPath");
    }
    createLogoWithTooltip(parent, className, seoAltImgDescEnd) {
        seoAltImgDescEnd = ("" == seoAltImgDescEnd)?
            "" : " " + seoAltImgDescEnd;
        createImg(
            parent,
            className + "_media",
            this.getTooltipText() + seoAltImgDescEnd,
            this.getLogoMediaPath()
        );
        createTextTooltip(
            parent,
            className + "_tooltip",
            this.getTooltipText()
        );
    }
}