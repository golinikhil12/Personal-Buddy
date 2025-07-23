const CACHE_NAME = 'personalbuddy-cache-v1';
const urlsToCache = [
  '/',
  '/static/manifest.json',
  '/static/style.css',
  '/static/main.js'
];

// Install service worker
self.addEventListener('install', event => {
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then(cache => cache.addAll(urlsToCache))
  );
});

// Fetch from cache
self.addEventListener('fetch', event => {
  event.respondWith(
    caches.match(event.request)
      .then(response => response || fetch(event.request))
  );
});
