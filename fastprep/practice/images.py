"""Source screenshots: serve from a local cache, fetch once if missing.

1619 problems carry 2025 screenshots of the real assessment, referenced as
paths like /api/problem-source-images/<id>/<n>. They are not in the database,
so the first view of a problem fetches its images from fastprep.io and writes
them to cache/images/. Every later view is local.

This is the only outbound traffic the app makes. It is rate-limited to 3
requests per second, single-flight per URL, and never re-fetches a cached file.
"""

from __future__ import annotations

import os
import re
import threading
import time
import urllib.error
import urllib.request

BASE = "https://www.fastprep.io"
HERE = os.path.dirname(os.path.abspath(__file__))
CACHE_DIR = os.environ.get("FP_IMAGE_CACHE") or os.path.join(HERE, "cache", "images")


def set_cache_dir(path: str) -> None:
    """Point the cache somewhere else - a Docker volume, usually."""
    global CACHE_DIR
    CACHE_DIR = os.path.abspath(path)
    os.makedirs(CACHE_DIR, exist_ok=True)
RATE = 3.0                       # requests per second, hard ceiling
TIMEOUT = 45           # their image endpoint is a cold serverless function
UA = ("Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36")

_SAFE = re.compile(r"^[A-Za-z0-9._-]+$")
_lock = threading.Lock()
_last = [0.0]
_inflight: dict[str, threading.Lock] = {}
_inflight_guard = threading.Lock()

SNIFF = [(b"\x89PNG\r\n\x1a\n", "image/png"), (b"\xff\xd8\xff", "image/jpeg"),
         (b"GIF8", "image/gif"), (b"RIFF", "image/webp")]


class ImageError(Exception):
    pass


def cache_path(problem_id: str, index: int) -> str:
    if not _SAFE.match(problem_id or "") or not (0 <= int(index) < 100):
        raise ImageError("bad image reference")
    return os.path.join(CACHE_DIR, "%s-%d" % (problem_id, int(index)))


def content_type(blob: bytes) -> str:
    for magic, mime in SNIFF:
        if blob.startswith(magic):
            return mime
    return "application/octet-stream"


def _throttle() -> None:
    with _lock:
        gap = 1.0 / RATE
        wait = _last[0] + gap - time.monotonic()
        if wait > 0:
            time.sleep(wait)
        _last[0] = time.monotonic()


def get(problem_id: str, index: int, allow_fetch: bool = True) -> tuple[bytes, str, bool]:
    """Returns (bytes, content-type, from_cache)."""
    path = cache_path(problem_id, index)
    if os.path.exists(path) and os.path.getsize(path) > 0:
        with open(path, "rb") as f:
            blob = f.read()
        return blob, content_type(blob), True
    if not allow_fetch:
        raise ImageError("not cached, and fetching is disabled")

    with _inflight_guard:                       # one fetch per image, not one per tab
        lock = _inflight.setdefault(path, threading.Lock())
    with lock:
        if os.path.exists(path) and os.path.getsize(path) > 0:
            with open(path, "rb") as f:
                blob = f.read()
            return blob, content_type(blob), True
        url = "%s/api/problem-source-images/%s/%d" % (BASE, problem_id, int(index))
        req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "image/*"})
        blob = mime = None
        last = None
        for attempt in range(2):            # a cold start often eats the first try
            _throttle()
            try:
                with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
                    blob = resp.read()
                    mime = resp.headers.get("Content-Type") or content_type(blob)
                break
            except urllib.error.HTTPError as e:
                raise ImageError("upstream returned %s" % e.code)
            except Exception as e:
                last = e
        if blob is None:
            raise ImageError("could not fetch: %s" % last)
        if not blob:
            raise ImageError("upstream returned an empty image")
        os.makedirs(CACHE_DIR, exist_ok=True)
        tmp = path + ".part"
        with open(tmp, "wb") as f:
            f.write(blob)
        os.replace(tmp, path)
        return blob, mime.split(";")[0].strip(), False


def cached_count() -> int:
    if not os.path.isdir(CACHE_DIR):
        return 0
    return sum(1 for n in os.listdir(CACHE_DIR) if not n.endswith(".part"))


def prefetch(pairs, log=print) -> tuple[int, int]:
    """Warm the cache for (problem_id, index) pairs. Used by --prefetch-images."""
    done = failed = 0
    total = len(pairs)
    for n, (pid, idx) in enumerate(pairs, 1):
        try:
            _, _, from_cache = get(pid, idx)
            done += 1
            if n % 50 == 0 or n == total:
                log("  %d/%d cached (%d failed)" % (n, total, failed))
        except ImageError as e:
            failed += 1
            log("  ! %s/%d: %s" % (pid, idx, e))
    return done, failed
