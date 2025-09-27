export async function getUrlResponse(url) {
    const response = await fetch(url);
    if (!response.ok) {
        return `Error: ${response.status}`;
    }
    return await response.text();
}