export function cancelPromise(promise) {
    if (promise != null) {
        console.log("promise cancelled")
        promise.cancel();
    }
}