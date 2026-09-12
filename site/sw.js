/* sw.js — keep the ~10 MB in-browser Python interpreter around.
 *
 * Pyodide is the only thing this worker ever touches: any URL containing
 * "/pyodide/" (the vendored copy in the container AND the CDN copy for plain
 * file:// dev) is served cache-first. It is downloaded once, stored in the
 * Cache Storage API, and every later visit loads straight from disk — even
 * offline. Everything else — the app pages and the /api/state sync — passes
 * straight through untouched, so your code/notes/progress are never cached.
 *
 * Bump the version below whenever pyrun.js moves to a new Pyodide version;
 * activate() then discards the stale copy automatically.
 */
'use strict';

const CACHE = 'amzoa-pyodide-v0.26.4';
const PREFIX = 'amzoa-';

self.addEventListener('install', () => self.skipWaiting());

self.addEventListener('activate', (e) => {
  e.waitUntil(
    caches.keys()
      .then((keys) => Promise.all(
        keys.filter((k) => k.startsWith(PREFIX) && k !== CACHE)
            .map((k) => caches.delete(k))))
      .then(() => self.clients.claim())
  );
});

self.addEventListener('fetch', (e) => {
  if (e.request.url.indexOf('/pyodide/') === -1) return;   // app/state traffic: ignore
  e.respondWith(
    caches.match(e.request).then((hit) => {
      if (hit) return hit;                                 // cache-first
      return fetch(e.request).then((resp) => {
        if (!resp) return resp;
        if (resp.type === 'opaque' || resp.status === 200) {
          const copy = resp.clone();
          caches.open(CACHE).then((c) => c.put(e.request, copy));
        }
        return resp;
      });
    })
  );
});