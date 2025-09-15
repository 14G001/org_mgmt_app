import { getUrlParam } from "./utils/url.js";

export function redirect(url) {
    window.location.href = url;
}
export function redirectToOriginalWebsite() {
    let nextUrl = getUrlParam(window, "next_url");
    if (!nextUrl) {
        nextUrl = "/";
    }
    redirect(nextUrl);
}