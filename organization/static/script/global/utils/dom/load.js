let toProcessOnDomLoadFinish = [];

document.addEventListener("DOMContentLoaded", onDomContentLoaded);

export function addActionToProcessOnDomLoadFinish(action) {
    toProcessOnDomLoadFinish.push(action);
}

function onDomContentLoaded() {
    toProcessOnDomLoadFinish.forEach(action => action());
}