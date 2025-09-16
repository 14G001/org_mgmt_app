export function getAppName() {
    return window.location.pathname.split("/")[1];
}