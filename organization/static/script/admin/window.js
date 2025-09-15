import { createElement, getByTag } from "../global/utils/dom/dom.js";

class Window {
    constructor(element, exitButton) {
        this.element = element;
        this.exitButton = exitButton;
    }
    close() {
        this.exitButton.click();
    }
}

export function createWindow(windowClassName) {
    let windowContainer = createElement(getByTag("body")[0], "div", "window_container");
    let exitButton = createElement(windowContainer, "button", "window_cancel_button");
    exitButton.innerText = "X";
    exitButton.onclick = ()=> {
        windowContainer.remove();
        document.onkeydown = ()=>{};
    }
    document.onkeydown = (event)=>{
        if (!["Escape","Esc"].includes(event.key)) {
            return;
        }
        exitButton.click();
    }
    const windowElement = createElement(windowContainer, "div", windowClassName);
    const windowInfo = new Window(windowElement, exitButton);
    return windowInfo;
}