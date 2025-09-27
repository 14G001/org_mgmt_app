export function getCookies() {
    return Object.fromEntries(
        document.cookie.split("; ")
            .map(cookie => cookie.split('='))
    )
}