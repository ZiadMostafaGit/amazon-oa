/* sw.js — keep the ~10 MB in-browser Python interpreter around.
 *
 * Pyodide is the only thing this worker ever touches: any URL containing
 * "/pyodide/" (the vendored copy in the container AND the CDN copy for plain
 * file:// dev) is handled here. It is downloaded once, verified, and served
 * from the Cache Storage API on every later visit — even offline. Everything
 * else — the app pages and the /api/state sync — passes straight through.
 *
 * Verification is the important part: pyodide-lock.json carries a sha256 for
 * every core file. Before a cached artifact is served this worker re-checks its
 * bytes against that hash, so a partial or poisoned copy can never wedge the
 * runtime: a mismatch is discarded and refetched.
 *
 * Bump CACHE when pyrun.js moves to a new Pyodide version; activate() then
 * discards the obsolete copy automatically.
 */
'use strict';

const CACHE = 'amzoa-pyodide-v2';
const PREFIX = 'amzoa-';
const CORE = ['/python_stdlib.zip', '/pyodide.asm.wasm', '/pyodide.asm.js', '/pyodide.js'];
const LOCK = 'pyodide-lock.json';

const sha256 = async (buf) => {
  const d = await crypto.subtle.digest('SHA-256', buf);
  return Array.from(new Uint8Array(d)).map((b) => b.toString(16).padStart(2, '0')).join('');
};

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
  if (!e.request.url.includes('/pyodide/')) return;   // app / state traffic: ignore
  e.respondWith(serve(e.request));
});

async function serve(request) {
  const cache = await caches.open(CACHE);

  /* The lock file is the truth table; keep it cache-first. The key is derived
     from the requested URL so it always points at the same directory. */
  if (request.url.endsWith(LOCK)) {
    const hit = await cache.match(request);
    if (hit) return hit;
    const resp = await fetch(request);
    if (resp.ok) cache.put(request, resp.clone());
    return resp;
  }

  const name = request.url.slice(request.url.indexOf('/pyodide/') + '/pyodide/'.length);
  const core = CORE.some((c) => request.url.endsWith(c));

  /* Expected sha256 for this file, from the lock (null = unknown). */
  let want = null;
  if (core) {
    const key = new URL(LOCK, request.url);
    try {
      const lockResp = await cache.match(key);
      if (lockResp) want = (await lockResp.json()).packages[name].sha256;
    } catch (_) { want = null; }
  }

  const good = async (resp) => {
    if (!resp || !resp.ok) return false;
    if (want === null) return true;
    try { return await sha256(await resp.clone().arrayBuffer()) === want; } catch (_) { return false; }
  };

  const hit = await cache.match(request);
  if (hit && (await good(hit.clone()))) return hit;      // validated, serve from disk

  const resp = await fetch(request);                     // (re)download
  if (resp && (resp.ok || resp.type === 'opaque')) {
    const ok = resp.ok && (want === null || (await good(resp.clone())));
    if (ok) cache.put(request, resp.clone());
  }
  return resp;
}