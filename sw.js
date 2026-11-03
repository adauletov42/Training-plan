const CACHE = 'training-v9';

// Всё приложение локально: внешних зависимостей больше нет, supabase-js и
// шрифт иконок лежат в vendor/. Раньше их адреса на CDN стояли в этом же
// addAll, и одна неудачная загрузка срывала установку целиком — кэш оставался
// пустым вместе с index.html, и офлайна не было вообще.
const CORE = [
  '/Training-plan/',
  '/Training-plan/index.html',
  '/Training-plan/manifest.json',
  '/Training-plan/icon-192.png',
  '/Training-plan/icon-512.png',
  '/Training-plan/vendor/supabase.js',
  '/Training-plan/vendor/tabler-icons-subset.css',
  '/Training-plan/vendor/tabler-icons-subset.woff2',
];

const OPTIONAL = [];

self.addEventListener('install', e => {
  e.waitUntil((async () => {
    const c = await caches.open(CACHE);
    await c.addAll(CORE);
    await Promise.allSettled(OPTIONAL.map(u => c.add(u)));
    await self.skipWaiting();
  })());
});

self.addEventListener('activate', e => {
  e.waitUntil(caches.keys().then(keys =>
    Promise.all(keys.filter(k => k !== CACHE).map(k => caches.delete(k)))
  ).then(() => self.clients.claim()));
});

self.addEventListener('fetch', e => {
  e.respondWith((async () => {
    try {
      const res = await fetch(e.request);
      if (res && res.status === 200) {
        const clone = res.clone();
        caches.open(CACHE).then(c => c.put(e.request, clone));
      }
      return res;
    } catch (err) {
      const hit = await caches.match(e.request);
      if (hit) return hit;
      // Переход по навигации офлайн: отдаём сохранённую оболочку приложения,
      // иначе пользователь получает ошибку сети вместо рабочего приложения.
      if (e.request.mode === 'navigate') {
        const shell = await caches.match('/Training-plan/index.html');
        if (shell) return shell;
      }
      throw err;
    }
  })());
});
