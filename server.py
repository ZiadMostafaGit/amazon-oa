#!/usr/bin/env python3
"""
Minimal server for Amazon OA practice.
Saves user state (code, notes, progress) to a JSON file on disk
so it survives browser restarts and works across devices.
"""

import json
import mimetypes
import os
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlparse

mimetypes.add_type("application/wasm", ".wasm")  # Pyodide falls back to a slower path without it

DATA_DIR = os.environ.get("DATA_DIR", "/data")
STATE_FILE = os.path.join(DATA_DIR, "state.json")
SITE_ROOT = os.environ.get("SITE_ROOT", "/usr/share/nginx/html")

_api_key = os.environ.get("API_KEY", "")  # optional: set to protect the endpoint


def _read_state():
    try:
        with open(STATE_FILE, "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}


def _write_state(data):
    os.makedirs(DATA_DIR, exist_ok=True)
    tmp = STATE_FILE + ".tmp"
    with open(tmp, "w") as f:
        json.dump(data, f, indent=1)
    os.replace(tmp, STATE_FILE)


class Handler(SimpleHTTPRequestHandler):
    # Keep-alive matters here: Pyodide pulls pyodide.asm.wasm (~9 MB),
    # python_stdlib.zip and the lock file, and the browser wants them on
    # parallel connections. HTTP/1.0 forced a new socket per asset.
    protocol_version = "HTTP/1.1"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=SITE_ROOT, **kwargs)

    def _send_json(self, code, obj):
        body = json.dumps(obj).encode()
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)

    def _is_state_api(self, path):
        # The page finds the API by probing candidates, so accept any spelling:
        # /api/state, /site/api/state, with or without a trailing slash.
        p = path.rstrip("/")
        return p == "/api/state" or p.endswith("/site/api/state")

    def send_head(self):
        # Both do_GET and do_HEAD route through here, so this is the one place
        # that sees every static response.
        self._immutable = "/vendor/" in urlparse(self.path).path
        return super().send_head()

    def end_headers(self):
        # Vendored deps (CodeMirror, Pyodide's ~10 MB runtime) never change
        # within a build, so browsers may keep them for a year without ever
        # re-downloading. Everything else keeps the usual Last-Modified
        # conditional caching.
        #
        # This MUST hang off end_headers, not send_head: send_header() appends
        # to the same buffer that send_response() writes the status line into,
        # so adding a header *before* delegating to super().send_head() emitted
        # the header first and the status line second. Browsers read that as
        # HTTP/0.9 — no status, no Content-Type — which is why Pyodide's wasm
        # silently failed to instantiate under the container.
        if getattr(self, "_immutable", False):
            self._immutable = False
            self.send_header("Cache-Control", "public, max-age=31536000, immutable")
        super().end_headers()

    def do_GET(self):
        path = urlparse(self.path).path

        if self._is_state_api(path):
            if _api_key and self.headers.get("X-API-Key") != _api_key:
                return self._send_json(401, {"error": "unauthorized"})
            return self._send_json(200, _read_state())

        # Serve the app — redirect bare / to /site/
        if path == "/":
            self.send_response(302)
            self.send_header("Location", "/site/")
            self.send_header("Content-Length", "0")   # keep-alive needs a length
            self.end_headers()
            return

        return super().do_GET()

    def do_POST(self):
        path = urlparse(self.path).path

        if self._is_state_api(path):
            if _api_key and self.headers.get("X-API-Key") != _api_key:
                return self._send_json(401, {"error": "unauthorized"})
            length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(length)
            try:
                data = json.loads(body)
            except json.JSONDecodeError:
                return self._send_json(400, {"error": "invalid json"})
            _write_state(data)
            return self._send_json(200, {"ok": True})

        self.send_error(404)

    def log_message(self, fmt, *args):
        super().log_message(fmt, *args)


def main():
    port = int(os.environ.get("PORT", "80"))
    os.makedirs(DATA_DIR, exist_ok=True)
    print(f"Serving {SITE_ROOT} on :{port}  (state → {STATE_FILE})")
    # Threaded: a single-threaded server serialises the runtime download
    # behind every other asset, which stalls the page for the whole ~10 MB.
    server = ThreadingHTTPServer(("0.0.0.0", port), Handler)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down.")
        server.server_close()


if __name__ == "__main__":
    main()
