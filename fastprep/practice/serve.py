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
import solutions as solutions_mod
import topics as topics_mod
sys.path.insert(0, os.path.join(HERE, "tools"))
from gaps import gaps_for

STATIC = os.path.join(HERE, "static")
mimetypes.add_type("application/javascript", ".js")

BANK: fpdb.Bank
PROGRESS: progress_mod.Progress
ALLOW_FETCH = True
BASE_PATH = ""          # e.g. "/site" when a reverse proxy mounts the app there


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
    has_solution = (q.get("hasSolution") or [""])[0] in ("1", "true", "yes")
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
    if has_solution:
        # another id scope, intersected with whatever the progress facets left
        verified = solutions_mod.verified_ids()
        f["ids"] = sorted(set(f["ids"]) & verified) if f.get("ids") is not None else sorted(verified)
    sort = (q.get("sort") or ["recent"])[0]
    direction = (q.get("dir") or [""])[0]
    limit = max(1, min(int((q.get("limit") or ["50"])[0] or 50), 500))
    offset = max(0, int((q.get("offset") or ["0"])[0] or 0))
    return f, sort, limit, offset, direction


def _problem_payload(detail: dict) -> dict:
    """Everything the problem view needs, in one place.

    Both the JSON endpoint and the inlined first paint go through here - when
    they were built separately, the inlined copy silently lost the stored
    solution and the user's own test cases.
    """
    pid = detail["id"]
    detail["languages"] = languages.catalogue(detail)
    detail["cases"] = BANK.runnable_cases(detail)
    detail["customCases"] = PROGRESS.cases(pid)
    detail["generatedCases"] = solutions_mod.generated_cases(pid)
    detail["progress"] = PROGRESS.get(pid)
    detail["solution"] = solutions_mod.get(pid, detail.get("practiceFormat") or "algorithm")
    # the canon topics this problem practises: the tags under the statement
    # link straight into the study space
    detail["studyTopics"] = topics_mod.topics_for(pid)
    # say what this problem does not have, rather than rendering empty sections
    detail["gaps"] = gaps_for(detail)
    return detail


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
    # Everything this app answers at its own root. Anything else in the first
    # segment can only be a mount prefix a proxy added.
    ROUTES = {"api", "app.js", "editor.js", "study.js", "timer.js", "pyenv.js",
              "styles.css", "index.html", "vendor", "favicon.ico"}

    def _strip_base(self, path: str) -> str:
        """Remove a mount prefix that a reverse proxy forwards verbatim.

        nginx `proxy_pass http://app;` (no trailing slash) passes /site/api/x
        through unchanged; with a trailing slash it strips the prefix. Both
        have to work, and a deployment should not break because an env var was
        forgotten - so an explicit --base-path wins, and otherwise any first
        segment that is not one of this app's own routes is treated as a mount
        prefix when what follows IS one.
        """
        if BASE_PATH and (path == BASE_PATH or path.startswith(BASE_PATH + "/")):
            return path[len(BASE_PATH):] or "/"
        # a proxy that announces its mount point is believed before guessing
        announced = (self.headers.get("X-Forwarded-Prefix") or "").rstrip("/")
        if announced and (path == announced or path.startswith(announced + "/")):
            return path[len(announced):] or "/"
        segments = path.lstrip("/").split("/")
        for i, seg in enumerate(segments):
            if seg in self.ROUTES:
                return "/" + "/".join(segments[i:]) if i else path
        # nothing recognisable, but a directory-style path can only be the
        # mount root: /site/ , /a/b/ , ...
        if path.endswith("/"):
            return "/"
        return path

    def do_GET(self):
        url = urlparse(self.path)
        # /site -> /site/ , so the page's relative URLs resolve inside the
        # mount point instead of one level above it. Only for a SINGLE unknown
        # segment: /site/nope is a typo and must stay a 404, not silently
        # redirect into the app.
        seg = url.path.strip("/")
        single = seg != "" and "/" not in seg
        # ...but never for something that exists, or that looks like a file:
        # /_selftest.html is a page, not a mount point.
        looks_like_a_file = "." in seg or os.path.isfile(os.path.join(STATIC, seg))
        if single and not url.path.endswith("/") and not looks_like_a_file \
                and seg not in self.ROUTES:
            target = url.path + "/" + (("?" + url.query) if url.query else "")
            self.send_response(301)
            self.send_header("Location", target)
            self.send_header("Content-Length", "0")
            self.end_headers()
            return
        path, q = self._strip_base(url.path), parse_qs(url.query)
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
                "solutions": solutions_mod.stats(),
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
            return self._json(_problem_payload(detail))
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
        if path == "/api/topics":
            return self._json(topics_mod.listing(PROGRESS, BANK))
        if path.startswith("/api/topics/"):
            slug = path[len("/api/topics/"):].strip("/")
            out = topics_mod.detail(slug, BANK, PROGRESS)
            if not out:
                return self._error(404, "no topic %r" % slug)
            return self._json(out)
        if path == "/api/progress":
            return self._json({"items": PROGRESS.all(), "stats": PROGRESS.stats()})
        if path == "/api/progress/export":
            return self._json(PROGRESS.export(), extra={
                "Content-Disposition": 'attachment; filename="fastprep-progress.json"'})
        return self._error(404, "no such endpoint")

    # ----------------------------------------------------------------- POST
    def do_POST(self):
        url = urlparse(self.path)
        url = url._replace(path=self._strip_base(url.path))
        try:
            body = self._body()
        except Exception as e:
            return self._error(400, "bad request body: %s" % e)
        try:
            if url.path == "/api/run":
                return self._run(body)
            if url.path == "/api/fuzz":
                return self._fuzz(body)
            if url.path == "/api/scratch":
                return self._scratch(body)
            if url.path == "/api/script":
                return self._script(body)
            if url.path.startswith("/api/cases/"):
                return self._cases(url.path[len("/api/cases/"):], body)
            if url.path.startswith("/api/study/"):
                slug = url.path[len("/api/study/"):].strip("/")
                if not topics_mod.index()["bySlug"].get(slug):
                    return self._error(404, "no topic %r" % slug)
                fields = {k: body[k] for k in ("status", "notes", "checked", "scratch")
                          if k in body}
                return self._json(PROGRESS.topic_update(slug, **fields))
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

    def _cases(self, pid: str, body: dict):
        """Add, edit or delete one of your own test cases for a problem."""
        detail = BANK.detail(pid)
        if not detail:
            return self._error(404, "no problem with id %r" % pid)
        action = (body.get("action") or "add").lower()
        if action == "delete":
            PROGRESS.delete_case(int(body["caseId"]))
        elif action == "update":
            PROGRESS.update_case(int(body["caseId"]), body.get("inputs"),
                                 body.get("expected"), body.get("note"))
        elif action == "add":
            inputs = body.get("inputs") or []
            if not isinstance(inputs, list):
                return self._error(400, "inputs must be a list")
            # a case with no expected value is still useful: it runs and shows
            # what your code returns, which is how you explore an edge case
            PROGRESS.add_case(pid, inputs, body.get("expected") or "", body.get("note") or "")
        else:
            return self._error(400, "unknown action %r" % action)
        return self._json({"customCases": PROGRESS.cases(pid)})

    def _fuzz(self, body: dict):
        """Your code against the stored reference, on generated inputs.

        Only offered where a VERIFIED reference exists: fuzzing against an
        unverified one would report disagreements that mean nothing.
        """
        pid = body.get("problemId")
        detail = BANK.detail(pid) if pid else None
        if not detail:
            return self._error(404, "no problem with id %r" % pid)
        if detail.get("practiceFormat") == "tabular":
            return self._error(400, "random testing is for algorithm problems")
        sol = solutions_mod.get(pid)
        if not sol or not sol.get("verified"):
            return self._error(400, "no verified reference solution for this problem, so "
                                    "there is nothing to compare against")
        cases = BANK.runnable_cases(detail)
        if not cases:
            return self._error(400, "this problem declares no inputs to generate")
        out_type = (detail.get("examples") or [{}])[0].get("outputType") or "int"
        result = runner.run_diff(body.get("code") or "", sol["code"],
                                 detail.get("functionName") or "solve",
                                 cases[0]["inputs"], out_type,
                                 trials=int(body.get("trials") or 300),
                                 budget=float(body.get("budget") or 6),
                                 seed=int(body.get("seed") or 1234))
        result["inputNames"] = [i.get("name") for i in cases[0]["inputs"]]
        result["inputTypes"] = [i.get("type") for i in cases[0]["inputs"]]
        result["sandbox"] = runner.sandbox_kind()
        result["sandboxNote"] = runner.sandbox_note()
        result["caveat"] = ("Inputs are generated from the declared types only, so some break "
                            "the problem's own rules; any input the reference rejects is "
                            "skipped rather than counted.")
        return self._json(result)

    def _script(self, body: dict):
        """Run the editor's code as a program, for its prints. No cases."""
        pid = body.get("problemId")
        if pid and not BANK.detail(pid):
            return self._error(404, "no problem with id %r" % pid)
        result = runner.run_script(body.get("code") or "")
        result["sandbox"] = runner.sandbox_kind()
        result["sandboxNote"] = runner.sandbox_note()
        return self._json(result)

    def _scratch(self, body: dict):
        pid = body.get("problemId")
        snippet = (body.get("snippet") or "").strip()
        if not snippet:
            return self._error(400, "nothing to evaluate")
        if pid and not BANK.detail(pid):
            return self._error(404, "no problem with id %r" % pid)
        result = runner.run_snippet(body.get("code") or "", snippet)
        result["sandbox"] = runner.sandbox_kind()
        result["sandboxNote"] = runner.sandbox_note()
        return self._json(result)

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
            include = (body.get("include") or "all").lower()
            cases = [] if include == "custom" else BANK.runnable_cases(detail)
            if include == "all":
                out_t = ((detail.get("examples") or [{}])[0] or {}).get("outputType") or "int"
                for g in solutions_mod.generated_cases(pid):
                    cases.append({"id": g["id"], "inputs": g["inputs"],
                                  "outputType": out_t, "expectedRaw": g["expectedRaw"],
                                  "generated": True})
            if include in ("all", "custom"):
                # a custom case inherits the problem's declared output type
                out_type = ((detail.get("examples") or [{}])[0] or {}).get("outputType") or "int"
                for c in PROGRESS.cases(pid):
                    cases.append({"id": "custom-%d" % c["caseId"], "inputs": c["inputs"],
                                  "outputType": out_type, "expectedRaw": c["expectedRaw"],
                                  "custom": True, "note": c["note"]})
            if not cases:
                return self._error(400, "nothing to run: this problem has no visible "
                                        "examples and you have added no cases")
            result = runner.run_python(code, cases, detail.get("functionName") or "solve")
            by_id = {str(c["id"]): c for c in cases}
            for r in result.get("results") or []:
                src = by_id.get(str(r.get("id"))) or {}
                r["custom"] = bool(src.get("custom"))
                r["generated"] = bool(src.get("generated"))
                if src.get("note"):
                    r["note"] = src["note"]
                if not src.get("expectedRaw"):
                    r["ok"] = None            # nothing to compare against: informational
                    r["expected"] = None
        else:
            return self._error(400, "%s is not executable here" % spec["label"])

        results = result.get("results") or []
        judged = [r for r in results if r.get("ok") is not None]
        passed = sum(1 for r in judged if r.get("ok"))
        PROGRESS.save_submission(pid, lang, code,
                                 passed if results else None,
                                 len(results) if results else None)
        result.update({
            "passed": passed, "total": len(judged),
            "sandbox": runner.sandbox_kind(),
            "sandboxNote": runner.sandbox_note(),
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
                    boot["detail"] = _problem_payload(detail)
            # the study space paints on the first frame too, rather than
            # flashing an empty pane while it fetches its own chapter
            study = (q.get("study") or [""])[0]
            if study:
                boot["topics"] = topics_mod.listing(PROGRESS, BANK)
                if study != "all":
                    boot["topic"] = topics_mod.detail(study, BANK, PROGRESS)
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
    ap.add_argument("--image-cache", default=None,
                    help="where to keep fetched source screenshots "
                         "(default: cache/images next to this file)")
    ap.add_argument("--host", default="127.0.0.1")
    ap.add_argument("--port", type=int, default=8900)
    ap.add_argument("--open", action="store_true", help="open a browser")
    ap.add_argument("--base-path", default=os.environ.get("FP_BASE_PATH", ""),
                    help="mount point, when a reverse proxy forwards the prefix "
                         "verbatim: --base-path /site")
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

    global BASE_PATH
    trimmed = (args.base_path or "").strip("/")
    BASE_PATH = "/" + trimmed if trimmed else ""
    if args.image_cache:
        images.set_cache_dir(args.image_cache)
    os.makedirs(os.path.dirname(os.path.abspath(args.progress_db)) or ".", exist_ok=True)
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
    if BASE_PATH:
        print("  mounted   under %s (the proxy is expected to forward that prefix)" % BASE_PATH)
    print("  sandbox   %s   python=yes java=%s pandas=%s   %ds wall / %ds cpu / %d MB"
          % (env["sandbox"], "yes" if env["java"] else "no",
             "yes" if env["pandas"] else "no",
             env["wallTimeout"], env["cpuSeconds"], env["memoryMB"]))
    if env["sandbox"] == "bubblewrap-shared-net":
        print("  WARNING   this machine will not let the sandbox create its own network")
        print("            namespace (bwrap: loopback: Failed RTM_NEWADDR), so user code")
        print("            SHARES this host's network. Everything else is still isolated.")
        print("            In Docker this is what security_opt: seccomp/apparmor is for.")
    elif env["sandbox"] != "bubblewrap":
        print("  WARNING   no working bwrap here: user code runs in a plain subprocess")
        print("            with resource limits only - no namespace isolation.")
    print("  images    %d cached in %s, fetching %s"
          % (images.cached_count(), images.CACHE_DIR,
             "enabled" if ALLOW_FETCH else "disabled"))
    sol = solutions_mod.stats()
    print("  solutions %d stored, %d verified against their visible examples (of %d targeted)"
          % (sol["stored"], sol["verified"], sol["targeted"]))
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
