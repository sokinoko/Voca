const CACHE = 'voca-v5';   // v4에 갇힌 폰이 새 워커를 받으며 옛 캐시를 버리게 올렸다
// 글꼴과 아이콘은 index.html 안에 base64로 박혀 있었다. 합쳐서 748 KB인데
// base64는 gzip이 안 먹어서, 그 덩어리 하나 때문에 첫 방문 전송량이 0.84 MB였다.
// 파일로 빼니 0.31 MB가 됐다. 대신 여기 적어 두어야 오프라인에서도 글꼴이 나온다.
const ASSETS = ['./', './index.html', './manifest.json',
                './hahmlet-400.woff2', './hahmlet-700.woff2',
                './icon-favicon.png', './icon-apple.png'];

self.addEventListener('install', e => {
  self.skipWaiting();
  e.waitUntil(caches.open(CACHE).then(c => c.addAll(ASSETS).catch(() => {})));
});

self.addEventListener('activate', e => {
  e.waitUntil(caches.keys().then(ks =>
    Promise.all(ks.filter(k => k !== CACHE).map(k => caches.delete(k)))
  ).then(() => self.clients.claim()));
});

// 캐시에 있으면 그것만 준다. **뒤에서 다시 받지 않는다.**
// 전에는 열 때마다 배경에서 전부 다시 받았다(0.31 MB + 글꼴). 그럴 필요가 없다 —
// 새 버전이 올라왔는지는 앱이 index.html의 ETag를 HEAD로 물어 알아내고(본문 0바이트),
// 「새로고침」을 누르면 캐시를 비우고 다시 받는다.
self.addEventListener('fetch', e => {
  const r = e.request;
  if (r.method !== 'GET') return;          // ETag를 묻는 HEAD 는 그냥 지나가게 둔다
  e.respondWith(
    caches.match(r).then(hit => hit || fetch(r).then(res => {
      if (res && res.status === 200 && res.type === 'basic') {
        const copy = res.clone();
        caches.open(CACHE).then(c => c.put(r, copy)).catch(() => {});
      }
      return res;
    }).catch(() => caches.match('./')))
  );
});

// 「새로고침」이 보내는 신호 — 캐시를 비운다. 다음 요청부터 새로 받는다
self.addEventListener('message', e => {
  if (e.data === 'flush') {
    e.waitUntil(caches.keys().then(ks => Promise.all(ks.map(k => caches.delete(k)))));
  }
});
