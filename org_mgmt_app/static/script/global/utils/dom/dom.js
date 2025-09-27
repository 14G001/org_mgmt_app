export function removeElementChilds(element) {
    while (element.firstChild) {
        element.removeChild(element.firstChild);
    }
}

export function setAttributesToElement(element, attributes) {
    for (const key in attributes) {
        element.setAttribute(key, attributes[key]);
    }
}

export function setStylesToElement(element, properties) {
    for (const key in properties) {
        element.style.setProperty(key, properties[key]);
    }
}

export function replaceNodeType(node, newNodeType) {
    const newElement = document.createElement(newNodeType);
    const numberOfElements = node.attributes.length;
    for (let elmCounter = 0; elmCounter < numberOfElements; elmCounter++) {
        const attr = node.attributes[elmCounter];
        newElement.setAttribute(attr.name, attr.value);
    }
    newElement.innerHTML = node.innerHTML;
    node.parentNode.replaceChild(newElement, node);
    return newElement;
}

export function createFragment() {
    return document.createDocumentFragment();
}

export function getById(id) {
    return document.getElementById(id);
}

export function getByClass(className) {
    return document.getElementsByClassName(className);
}

export function removeTextNodes(nodes) {
    const finalNodes = [];
    const len = nodes.length;
    for (let nodeCtr = 0; nodeCtr < len; nodeCtr++) {
        const node = nodes[nodeCtr];
        if (![Node.TEXT_NODE, Node.COMMENT_NODE].includes(node.nodeType)) {
            finalNodes.push(node);
        }
    }
    return finalNodes;
}

export function getByPosition(element, positions) {
    positions.forEach(pos => {
        element = removeTextNodes(element.childNodes)[pos];
    });
    return element;
}

export function getByTag(tagName) {
    return document.getElementsByTagName(tagName);
}

export function getGlobalVar(globalVar) {
    return getComputedStyle(document.documentElement).getPropertyValue(globalVar);
}

export function createElement(parent, elementType, className) {
    const element = document.createElement(elementType.toUpperCase());
    if (parent) {
        parent.appendChild(element);
    }
    if (className) {
        element.className = className;
    }
    return element;
}

export function createLink(parent, className, link) {
    const element = createElement(parent, "a", className);
    if (link) {
        element.setAttribute("href", link);
    }
    return element;
}

export function createText(parent, elementType, text, className) {
    const element = createElement(parent, elementType, className);
    element.innerText = text;
    return element;
}

export function createParagraph(parent, className, htmlContent) {
    const element = createElement(parent, "p", className);
    element.innerHTML = htmlContent;
    return element;
}

export function createImg(parent, className, seoAltImgDesc, source) {
    const element = createElement(parent, "img", className);
    setAttributesToElement(element, {
        alt : seoAltImgDesc,
        src : source
    });
    return element
}

export function createTooltip(parent, tooltip) {
    parent.onmouseenter = () => {
        tooltip.style.display = "block";
    }
    parent.onmouseleave = () => {
        tooltip.style.display = "none";
    }
    tooltip.style.display = "none";
    return tooltip;
}

export function createTextTooltip(parent, className, text) {
    return createTooltip(parent, createText(parent, "div", text, className));
}

function getIfNotTrue(value, equalValue, distinctValue) {
    return (value == equalValue)?
        distinctValue :
        equalValue;
}

function createSectionToggle(button, sections, arrow, text, startsShown) {
    const sectionToggleInfo = [];
    for (const sectionNum in sections) {
        const section = sections[sectionNum];
        sectionToggleInfo.push({
            originalDisplayType: section.style.display,
            section: section
        });
        arrow.style.transform = "rotate(180deg)";
        if (!startsShown) {
            section.style.display = "none";
        }
    }
    button.onclick = ()=>{
        for (const sectionNum in sectionToggleInfo) {
            const sectionInfo = sectionToggleInfo[sectionNum];
            const section = sectionInfo.section;
            section.style.display = getIfNotTrue(section.style.display, "none", sectionInfo.originalDisplayType);
            button.style.zIndex = (section.style.display == "none")? "0" : "1";
            arrow.style.transform = getIfNotTrue(arrow.style.transform, "none", "rotate(180deg)");
            if (text) {
                text.innerText = getIfNotTrue(text.innerText, "Show more", "Show less");
            }
        }
    };
}

export function createSectionToggleButton(button, sections, arrow, startsShown) {
    createSectionToggle(button, sections, arrow, null, startsShown);
}

export function createSectionToggleText(button, sections, arrow, text, startsShown) {
    createSectionToggle(button, sections, arrow, text, startsShown);
}