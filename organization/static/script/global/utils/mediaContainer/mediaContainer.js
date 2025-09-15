export class MediaContainer {
    constructor(mediaFileName, url) {
        this.mediaFileName = mediaFileName;
        this.url = url;
    }
    setMediaFileName(mediaFileName) {
        this.mediaFileName = mediaFileName;
    }
    getMediaFileName() {
        return this.mediaFileName;
    }
    getUrl() {
        return this.url;
    }
    getMediaPath() {
        throw new Error("Implement method MediaContainer.getMediaPath");
    }
}