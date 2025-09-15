import {FileImage} from "./type/image.js";
import {FileAudio} from "./type/audio.js";
import {FileVideo} from "./type/video.js";
import {isIn} from "../collection.js";

export class File {
    constructor(filePath) {
        this.name = filePath;
        if (filePath.split("/") != undefined) {
            this.name = filePath.split("/")[filePath.split("/").length - 1];
        }
        this.folder = filePath.replace(this.name, "");
        this.file = this.getFileType();
    }
    getFileType () {
        const fileFormat = this.getFileFormat();
        if (isIn(fileFormat, ["jpg", "png", "gif"])) {
            return new FileImage(this);
        }
        if (isIn(fileFormat, ["mp3", "wav"])) {
            return new FileAudio(this);
        }
        if (isIn(fileFormat, ["mp4"])) {
            return new FileVideo(this);
        }
        return null;
    }
    getFullPath () {
        return this.folder + this.name;
    }
    getFileFormat () {
        return this.name.split(".")[1];
    }
    getNode(parent, className, seoAltImgDesc) {
        return this.file.getNode(parent, className, seoAltImgDesc);
    }
}