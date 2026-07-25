const CACHE_NAME = "fotokitablur-v4";
const ASSETS_TO_CACHE = [
    "./",
    "./index.html",
    "./style.css",
    "./app.js",
    "./calibration.js",
    "./FOTO%20KITA%20BLUR%20-%20SAL%20PRIADI.mp3",
    "./Hidup%20jokowi%20%20sound%20meme.mp3"
];

async function safeFetch(event) {
    try {
        const url = new URL(event.request.url);
        if (url.protocol !== "http:" && url.protocol !== "https:") {
            return await fetch(event.request);
        }
        const response = await fetch(event.request);
        if (!response || response.status !== 200 || response.type !== "basic") {
            return response;
        }
        const responseToCache = response.clone();
        caches.open(CACHE_NAME).then((cache) => {
            cache.put(event.request, responseToCache);
        });
        return response;
    } catch (err) {
        return new Response("", { status: 504, statusText: "Gateway Timeout" });
    }
}

self.addEventListener("install", (event) => {
    event.waitUntil(
        caches.open(CACHE_NAME).then((cache) => {
            return cache.addAll(ASSETS_TO_CACHE);
        })
    );
    self.skipWaiting();
});

self.addEventListener("activate", (event) => {
    event.waitUntil(
        caches.keys().then((names) => {
            return Promise.all(
                names.filter((name) => name !== CACHE_NAME)
                     .map((name) => caches.delete(name))
            );
        })
    );
    self.clients.claim();
});

self.addEventListener("fetch", (event) => {
    if (event.request.url.startsWith("chrome-extension://")) return;
    event.respondWith(
        caches.match(event.request).then((response) => {
            if (response) return response;
            return safeFetch(event);
        })
    );
});