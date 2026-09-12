/* sw.js — retirement worker.
 *
 * Older versions cached the ~10 MB Python runtime here, but serving it from a
 * service worker proved fragile (mixed/MIME-mangled artifacts wedge Pyodide's
 * silent wasm loader). The runtime is now cached by plain immutable HTTP
 * responses on /vendor/ instead. This worker exists only to remove every
 * trace of the old one: purge the caches, unregister itself, reload clients.
 */
'use strict';

self.addEventListener('install', () => self.skipWaiting());

self.addEventListener('activate', (e) => {
  e.waitUntil((async () => {
    const keys = await caches.keys();
    await Promise.all(keys.filter((k) => k.indexOf('amzoa') === 0)
                          .map((k) => caches.delete(k)));
    await self.registration.unregister();
    const clients = await self.clients.matchAll({ type: 'window' });
    clients.forEach((c) => c.navigate(c.url));
  })());
});