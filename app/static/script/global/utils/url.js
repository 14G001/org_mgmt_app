import { getAppName } from "../app/appName.js";

export function getUrlResource(_window) {
    return _window.location.pathname.slice(
        `/${getAppName()}`.length);
}
export function getUrlParams(_window) {
    return _window.location.search;
}
export function getUrlResourceAndQParams(_window) {
    return `${getUrlResource(_window)}${getUrlParams(_window)}`;
}
export function getIsolatedUrlParams(_window) {
    return new URLSearchParams(getUrlParams(_window));
}
export function getUrlParam(_window, param) {
    return getIsolatedUrlParams(_window).get(param);
}