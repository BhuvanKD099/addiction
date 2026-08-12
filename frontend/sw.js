const CACHE_NAME = "addictionsense-pwa-v1";
const ASSETS_TO_CACHE = [
    "./",
    "./dashboard.html",
    "./addictionsense.html",
    "./patients.html",
    "./doctors.html",
    "./medications.html",
    "./counselling.html",
    "./appointments.html",
    "./progress.html",
    "./relapse.html",
    "./resources.html",
    "./reports.html",
    "./css/style.css",
    "./js/api.js",
    "./js/patient.js",
    "./js/doctor.js",
    "./manifest.json"
];

self.addEventListener("install", (event) => {
    event.waitUntil(
        caches.open(CACHE_NAME).then((cache) => {
            console.log("[PWA Service Worker] Caching App Shell");
            return cache.addAll(ASSETS_TO_CACHE);
        })
    );
    self.skipWaiting();
});

self.addEventListener("activate", (event) => {
    event.waitUntil(
        caches.keys().then((keyList) => {
            return Promise.all(
                keyList.map((key) => {
                    if (key !== CACHE_NAME) {
                        console.log("[PWA Service Worker] Removing old cache", key);
                        return caches.delete(key);
                    }
                })
            );
        })
    );
    self.clients.claim();
});

self.addEventListener("fetch", (event) => {
    if (event.request.method !== "GET") return;
    
    event.respondWith(
        fetch(event.request)
            .then((response) => {
                const responseClone = response.clone();
                caches.open(CACHE_NAME).then((cache) => {
                    cache.put(event.request, responseClone);
                });
                return response;
            })
            .catch(() => {
                return caches.match(event.request);
            })
    );
});
