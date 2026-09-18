#!/usr/bin/env python3
"""FastPrep practice - a local web app over the offline problem bank.

    python3 serve.py                 # http://127.0.0.1:8900
    python3 serve.py --port 9000 --open
    python3 serve.py --prefetch-images   # warm the image cache, then exit
    python3 serve.py --selftest          # run the test suite and exit

Nothing here writes to fastprep.db: it is opened read-only, and your progress
lives in progress.db next to this file.
"""

from __future__ import annotations

import argparse
import json
import mimetypes
import os
import sys
import threading
import traceback
import webbrowser
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs, urlparse

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import fpdb
import images
import languages
import progress as progress_mod
import runner

STATIC = os.path.join(HERE, "static")
mimetypes.add_type("application/javascript", ".js")

BANK: fpdb.Bank
PROGRESS: progress_mod.Progress
ALLOW_FETCH = True


# --------------------------------------------------------------------------
# request helpers
# --------------------------------------------------------------------------
def _filters_from_query(q: dict) -> tuple[dict, str, int, int, str]:
    """Query string -> filter dict. Repeated keys mean OR inside a facet;
    different keys mean AND across facets."""
    multi = lambda k: [v for v in q.get(k, []) if v != ""]
    f = {
        "company": multi("company"), "difficulty": multi("difficulty"),
        "platform": multi("platform"), "format": multi("format"),
        "stage": multi("stage"), "topic": multi("topic"),
        "employment": multi("employment"), "role": multi("role"),
        "q": (q.get("q") or [""])[0],
        "seenFrom": (q.get("seenFrom") or [""])[0],
        "seenTo": (q.get("seenTo") or [""])[0],
        "seenOnFrom": (q.get("seenOnFrom") or [""])[0],
        "seenOnTo": (q.get("seenOnTo") or [""])[0],
        "minSeen": (q.get("minSeen") or [""])[0],
        "maxSeen": (q.get("maxSeen") or [""])[0],
        "hasImages": (q.get("hasImages") or [""])[0] in ("1", "true", "yes"),
    }
    # progress facets live in the other database: resolve them to an id scope
    status = (q.get("status") or [""])[0]
    bookmarked = (q.get("bookmarked") or [""])[0] in ("1", "true", "yes")
    has_notes = (q.get("hasNotes") or [""])[0] in ("1", "true", "yes")
    if status or bookmarked or has_notes:
        if status == "none":
            touched = set(PROGRESS.ids_with(bookmarked=bookmarked, has_notes=has_notes))
            known = {r[0] for r in BANK.conn.execute(
                "SELECT id FROM problems")}
            with_status = {r["problem_id"] for r in PROGRESS.conn.execute(
                "SELECT problem_id FROM progress WHERE status IS NOT NULL")}
            f["ids"] = sorted(known - with_status)
        else:
            f["ids"] = PROGRESS.ids_with(status=status or None, bookmarked=bookmarked,
                                         has_notes=has_notes)
    sort = (q.get("sort") or ["recent"])[0]
    direction = (q.get("dir") or [""])[0]
    limit = max(1, min(int((q.get("limit") or ["50"])[0] or 50), 500))
    offset = max(0, int((q.get("offset") or ["0"])[0] or 0))
    return f, sort, limit, offset, direction


class Handler(BaseHTTPRequestHandler):
    protocol_version = "HTTP/1.1"
    server_version = "FastPrepPractice/1.0"

    # ------------------------------------------------------------- plumbing
    def log_message(self, fmt, *args):
        if os.environ.get("FP_VERBOSE"):
            super().log_message(fmt, *args)

    def _send(self, code: int, body: bytes, ctype: str, extra: dict | None = None):
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(body)))
        for k, v in (extra or {}).items():
            self.send_header(k, v)
        self.end_headers()
        if self.command != "HEAD":
            self.wfile.write(body)

    def _json(self, obj, code: int = 200, extra: dict | None = None):
        self._send(code, json.dumps(obj).encode("utf-8"), "application/json", extra)

    def _error(self, code: int, message: str):
        self._json({"error": message}, code)

    def _body(self) -> dict:
        n = int(self.headers.get("Content-Length") or 0)
        if n <= 0:
            return {}
        if n > 4_000_000:
            raise ValueError("request body too large")
        return json.loads(self.rfile.read(n) or b"{}")

    # ------------------------------------------------------------------ GET
    def do_GET(self):
        url = urlparse(self.path)
        path, q = url.path, parse_qs(url.query)
        try:
            if path.startswith("/api/"):
                return self._api_get(path, q)
            return self._static(path)
        except Exception:
            traceback.print_exc()
            return self._error(500, "internal error")

    do_HEAD = do_GET

    def _api_get(self, path: str, q: dict):
        if path == "/api/health":
            return self._json({
                "ok": True, "bank": BANK.path, "problems": BANK.facets()["meta"]["total"],
                "progressDb": PROGRESS.path, "imagesCached": images.cached_count(),
                "environment": languages.environment(),
            })
        if path == "/api/facets":
            out = BANK.facets()
            out["progress"] = self._progress_counts(out["meta"]["total"])
            return self._json(out)
        if path == "/api/problems":
            f, sort, limit, offset, direction = _filters_from_query(q)
            res = BANK.query(f, sort=sort, limit=limit, offset=offset, direction=direction)
            marks = PROGRESS.all()
            for item in res["items"]:
                item["progress"] = marks.get(item["id"])
            return self._json(res)
        if path.startswith("/api/problems/"):
            rest = path[len("/api/problems/"):]
            pid, _, tail = rest.partition("/")
            detail = BANK.detail(pid)
            if not detail:
                return self._error(404, "no problem with id %r" % pid)
            if tail == "neighbours":
                f, sort, _, _, direction = _filters_from_query(q)
                return self._json(BANK.neighbours(pid, f, sort, direction))
            detail["languages"] = languages.catalogue(detail)
            detail["cases"] = BANK.runnable_cases(detail)
            detail["progress"] = PROGRESS.get(pid)
            return self._json(detail)
        if path.startswith("/api/images/"):
            parts = path[len("/api/images/"):].split("/")
            if len(parts) != 2 or not parts[1].isdigit():
                return self._error(400, "expected /api/images/<problem-id>/<n>")
            try:
                blob, ctype, cached = images.get(parts[0], int(parts[1]),
                                                allow_fetch=ALLOW_FETCH)
            except images.ImageError as e:
                return self._error(404, str(e))
            return self._send(200, blob, ctype, {
                "Cache-Control": "public, max-age=604800",
                "X-Image-Source": "cache" if cached else "fetched"})
        if path == "/api/progress":
            return self._json({"items": PROGRESS.all(), "stats": PROGRESS.stats()})
        if path == "/api/progress/export":
            return self._json(PROGRESS.export(), extra={
                "Content-Disposition": 'attachment; filename="fastprep-progress.json"'})
        return self._error(404, "no such endpoint")

    # ----------------------------------------------------------------- POST
    def do_POST(self):
        url = urlparse(self.path)
        try:
            body = self._body()
        except Exception as e:
            return self._error(400, "bad request body: %s" % e)
        try:
            if url.path == "/api/run":
                return self._run(body)
            if url.path.startswith("/api/progress/"):
                pid = url.path[len("/api/progress/"):]
                if not BANK.detail(pid):
                    return self._error(404, "no problem with id %r" % pid)
                fields = {k: body[k] for k in ("status", "bookmarked", "notes") if k in body}
                if "code" in body and body.get("language"):
                    PROGRESS.save_submission(pid, body["language"], body["code"])
                return self._json(PROGRESS.update(pid, **fields))
            return self._error(404, "no such endpoint")
        except ValueError as e:
            return self._error(400, str(e))
        except Exception:
            traceback.print_exc()
            return self._error(500, "internal error")

    def _run(self, body: dict):
        pid = body.get("problemId")
        code = body.get("code") or ""
        lang = body.get("language") or "python"
        detail = BANK.detail(pid) if pid else None
        if not detail:
            return self._error(404, "no problem with id %r" % pid)

        catalogue = {l["id"]: l for l in languages.catalogue(detail)}
        spec = catalogue.get(lang)
        if not spec:
            return self._error(400, "unknown language %r for this problem" % lang)
        if not spec["runnable"]:
            return self._error(400, "%s cannot be executed here: %s"
                               % (spec["label"], spec.get("note") or ""))

        if spec["mode"] == "sql":
            result = runner.run_sql(code, detail.get("tabular") or {})
        elif spec["mode"] == "python":
            cases = BANK.runnable_cases(detail)
            if not cases:
                return self._error(400, "this problem has no visible examples to run")
            result = runner.run_python(code, cases, detail.get("functionName") or "solve")
        else:
            return self._error(400, "%s is not executable here" % spec["label"])

        results = result.get("results") or []
        passed = sum(1 for r in results if r.get("ok"))
        PROGRESS.save_submission(pid, lang, code,
                                 passed if results else None,
                                 len(results) if results else None)
        result.update({
            "passed": passed, "total": len(results),
            "sandbox": runner.sandbox_kind(),
            "disclaimer": "These are the problem's VISIBLE examples only. This bank "
                          "ships no hidden tests and no reference solution, so passing "
                          "them does not mean your solution is correct.",
        })
        return self._json(result)

    @staticmethod
    def _progress_counts(total: int) -> dict:
        """Counts for the progress facet. `none` means "no status anywhere in
        the bank", not "a row in progress.db whose status is null"."""
        stats = PROGRESS.stats()
        with_status = PROGRESS.conn.execute(
            "SELECT COUNT(*) FROM progress WHERE status IS NOT NULL").fetchone()[0]
        stats["none"] = total - with_status
        stats[""] = total
        return stats

    def _index(self):
        """index.html with the first screen's data inlined.

        Without this the page paints empty and then fills in after two round
        trips; with it the list is there in the first frame (and a headless
        screenshot shows something).
        """
        with open(os.path.join(STATIC, "index.html"), "r", encoding="utf-8") as f:
            html = f.read()
        q = parse_qs(urlparse(self.path).query)
        try:
            f_, sort, limit, offset, direction = _filters_from_query(q)
            listing = BANK.query(f_, sort=sort, limit=limit, offset=offset,
                                 direction=direction)
            marks = PROGRESS.all()
            for item in listing["items"]:
                item["progress"] = marks.get(item["id"])
            facets = BANK.facets()
            facets["progress"] = self._progress_counts(facets["meta"]["total"])
            boot = {"facets": facets, "list": listing,
                    "environment": languages.environment()}
            wanted = (q.get("id") or [""])[0]
            if wanted:
                detail = BANK.detail(wanted)
                if detail:
                    detail["languages"] = languages.catalogue(detail)
                    detail["cases"] = BANK.runnable_cases(detail)
                    detail["progress"] = PROGRESS.get(wanted)
                    boot["detail"] = detail
        except Exception:
            traceback.print_exc()
            boot = None
        tag = ("<script>window.__BOOT__=%s;</script>"
               % json.dumps(boot).replace("</", "<\\/")) if boot else ""
        html = html.replace("<script src=\"app.js\"></script>",
                            tag + "\n<script src=\"app.js\"></script>")
        return self._send(200, html.encode("utf-8"), "text/html; charset=utf-8",
                          {"Cache-Control": "no-cache"})

    # --------------------------------------------------------------- static
    def _static(self, path: str):
        if path in ("/", ""):
            path = "/index.html"
        if path == "/index.html":
            return self._index()
        rel = os.path.normpath(path.lstrip("/")).replace("\\", "/")
        if rel.startswith(".."):
            return self._error(403, "no")
        full = os.path.join(STATIC, rel)
        if not os.path.isfile(full):
            return self._error(404, "not found")
        ctype = mimetypes.guess_type(full)[0] or "application/octet-stream"
        with open(full, "rb") as f:
            blob = f.read()
        return self._send(200, blob, ctype, {"Cache-Control": "no-cache"})


# --------------------------------------------------------------------------
def _prefetch(bank: fpdb.Bank) -> int:
    pairs = []
    for r in bank.conn.execute(
            "SELECT id, json_extract(detail_json,'$.sourceImages') si FROM problems "
            "WHERE json_array_length(json_extract(detail_json,'$.sourceImages')) > 0"):
        for n, _ in enumerate(json.loads(r["si"])):
            if not os.path.exists(images.cache_path(r["id"], n)):
                pairs.append((r["id"], n))
    if not pairs:
        print("every source image is already cached (%d files)" % images.cached_count())
        return 0
    print("fetching %d image(s) at %.0f req/s - about %d min"
          % (len(pairs), images.RATE, round(len(pairs) / images.RATE / 60) or 1))
    done, failed = images.prefetch(pairs)
    print("done: %d cached, %d failed" % (done, failed))
    return 1 if failed else 0


def main() -> int:
    global BANK, PROGRESS, ALLOW_FETCH
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--db", default=fpdb.DEFAULT_DB, help="the FastPrep bank (read-only)")
    ap.add_argument("--progress-db", default=progress_mod.DEFAULT_PATH)
    ap.add_argument("--host", default="127.0.0.1")
    ap.add_argument("--port", type=int, default=8900)
    ap.add_argument("--open", action="store_true", help="open a browser")
    ap.add_argument("--offline", action="store_true",
                    help="never fetch images; serve only what is cached")
    ap.add_argument("--prefetch-images", action="store_true",
                    help="download every uncached source image, then exit")
    ap.add_argument("--selftest", action="store_true", help="run the tests, then exit")
    args = ap.parse_args()

    if args.selftest:
        import unittest
        loader = unittest.TestLoader()
        suite = loader.discover(os.path.join(HERE, "tests"), top_level_dir=HERE)
        ok = unittest.TextTestRunner(verbosity=2).run(suite).wasSuccessful()
        return 0 if ok else 1

    BANK = fpdb.Bank(args.db)
    PROGRESS = progress_mod.Progress(args.progress_db)
    ALLOW_FETCH = not args.offline

    if args.prefetch_images:
        return _prefetch(BANK)

    meta = BANK.facets()["meta"]
    env = languages.environment()
    url = "http://%s:%d/" % (args.host, args.port)
    print("FastPrep practice")
    print("  bank      %s  (read-only, %d problems, newest sighting %s)"
          % (BANK.path, meta["total"], meta["latest"]))
    print("  progress  %s" % PROGRESS.path)
    print("  sandbox   %s   python=yes java=%s pandas=%s   %ds wall / %ds cpu / %d MB"
          % (env["sandbox"], "yes" if env["java"] else "no",
             "yes" if env["pandas"] else "no",
             env["wallTimeout"], env["cpuSeconds"], env["memoryMB"]))
    if env["sandbox"] != "bubblewrap":
        print("  WARNING   bwrap not found: user code runs in a plain subprocess with")
        print("            resource limits only - no namespace isolation.")
    print("  images    %d cached, fetching %s" % (images.cached_count(),
                                                  "enabled" if ALLOW_FETCH else "disabled"))
    print("\n  -> %s\n" % url)

    httpd = ThreadingHTTPServer((args.host, args.port), Handler)
    httpd.daemon_threads = True
    if args.open:
        threading.Timer(0.5, lambda: webbrowser.open(url)).start()
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nbye")
    finally:
        httpd.server_close()
    return 0


if __name__ == "__main__":
    sys.exit(main())
