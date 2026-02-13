const CACHE_NAME = 'Hibi';
const ASSETS = [
    './index.html',
    './manifest.json',
    './icon.png'
];

// 安裝時快取檔案
self.addEventListener('install', (e) => {
    e.waitUntil(
        caches.open(CACHE_NAME).then((cache) => cache.addAll(ASSETS))
    );
    self.skipWaiting();
});

// 啟動時接管控制權
self.addEventListener('activate', (e) => {
    e.waitUntil(self.clients.claim());
});

// 攔截請求：有快取讀快取，沒快取讀網路
self.addEventListener('fetch', (e) => {
    e.respondWith(
        caches.match(e.request).then((response) => {
            return response || fetch(e.request);
        })
    );
});