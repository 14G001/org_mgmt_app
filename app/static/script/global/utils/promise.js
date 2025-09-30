export function cancelPromise(promise) {
    if (promise != null) {
        promise.cancel();
    }
}