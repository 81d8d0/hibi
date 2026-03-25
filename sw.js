// ▼▼▼ 每次更新網頁內容時，請修改這裡的版本號 ▼▼▼
const CACHE_NAME = 'Hibi';
// ▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲

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
    self.skipWaiting(); // 強制新的 SW 立即接管
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

// 攔截請求：改用「網路優先 (Network First)」策略
self.addEventListener('fetch', (e) => {
    e.respondWith(
        fetch(e.request)
            .then((response) => {
                // 網路連線成功，就把最新抓到的檔案更新到快取裡
                if (response && response.status === 200 && response.type === 'basic') {
                    const responseToCache = response.clone();
                    caches.open(CACHE_NAME).then((cache) => {
                        cache.put(e.request, responseToCache);
                    });
                }
                return response;
            })
            .catch(() => {
                // 網路斷線（離線狀態），退回使用快取檔案
                return caches.match(e.request);
            })
    );
});