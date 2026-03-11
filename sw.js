// ▼▼▼ 1. 這裡就是版本號，每次更新網頁內容時，請修改這裡 (例如 v1 -> v2) ▼▼▼
const CACHE_NAME = 'Hibi-v2'; 
// ▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲

const ASSETS = [
    './index.html',
    './manifest.json',
    './icon.png'
];

// 安裝時快取檔案
self.addEventListener('install', (e) => {
    console.log('[SW] 安裝新版本:', CACHE_NAME);
    e.waitUntil(
        caches.open(CACHE_NAME).then((cache) => cache.addAll(ASSETS))
    );
    self.skipWaiting();
});

// 啟動時接管控制權 (並刪除舊的快取)
self.addEventListener('activate', (e) => {
    e.waitUntil(
        caches.keys().then((keyList) => {
            return Promise.all(keyList.map((key) => {
                // 如果快取名稱跟現在的版本不一樣，就刪掉它
                if (key !== CACHE_NAME) {
                    console.log('[SW] 刪除舊快取:', key);
                    return caches.delete(key);
                }
            }));
        }).then(() => self.clients.claim())
    );
});

// 攔截請求
self.addEventListener('fetch', (e) => {
    e.respondWith(
        caches.match(e.request).then((response) => {
            return response || fetch(e.request);
        })
    );
});