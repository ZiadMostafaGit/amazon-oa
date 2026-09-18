# Amazon OA practice

56 Amazon / Siemens online-assessment problems transcribed from screenshots, each with a worked
solution and a step-by-step derivation, plus a Python editor and a test runner that executes real
CPython **in the browser**. No build step, no account; open `site/index.html` for a zero-backend
version, or run the Docker image for server-side persistence of your code and progress.

```
site/     the app (open site/index.html, or run the container)
images/   source screenshots and the cropped figures the problems refer to
video/    OCR transcripts of a recorded 42-minute attempt (the .mp4 itself is not kept here)
scripts/  vendor.sh — fetches the CDN assets so the container runs offline
docker/   nginx config
```

## Run it

**Directly** — open `site/index.html` in a browser. Needs internet the first time (CodeMirror,
JetBrains Mono, and ~10 MB of Pyodide come from CDNs and are then cached).

**In Docker** — self-contained, works with no internet at all, and **persists your code, notes and
progress on the server** so nothing is lost when you reopen it on another browser/device:

```sh
docker compose up --build -d      # then open http://localhost:8080
```

or without compose (mount a volume or all state is lost when the container is recreated):

```sh
docker build -t amazon-oa-practice .
docker run -d -p 8080:80 -v amazon-oa-data:/data --name amazon-oa amazon-oa-practice
```

The build fetches CodeMirror, the font and the Pyodide runtime into the image and rewrites the two
files that reference them, so the container never reaches the network at run time. State is written
to `/data/state.json` (an anonymous volume otherwise) by the tiny backend in `server.py`.

## Publish it to Docker Hub

Replace `YOURNAME` with your Docker Hub username.

```sh
docker login

# build for your own machine only
docker build -t YOURNAME/amazon-oa-practice:1.0 -t YOURNAME/amazon-oa-practice:latest .
docker push YOURNAME/amazon-oa-practice:1.0
docker push YOURNAME/amazon-oa-practice:latest
```

To make it run on Apple Silicon and ARM servers as well as x86, build multi-arch instead — this is
the version worth pushing if "anyone, anywhere" is the goal:

```sh
docker buildx create --use --name oabuilder            # once
docker buildx build --platform linux/amd64,linux/arm64 \
  -t YOURNAME/amazon-oa-practice:1.0 \
  -t YOURNAME/amazon-oa-practice:latest --push .
```

Anyone can then run it with:

```sh
docker run -d -p 8080:80 -v amazon-oa-data:/data YOURNAME/amazon-oa-practice
```

## What's in the app

- **56 problems** — 15 Amazon coding, 2 work simulation, 6 debugging projects, 5 Siemens,
  27 FastPrep, plus a frame-by-frame post-mortem of a real 60-minute attempt.
- **52 answer sets** — Hint 1 → Hint 2 → Solution → *Step by step*, the last deriving every formula
  and tracing the published sample numerically to its stated answer.
- **A Python editor** — Vim mode, stdlib-wide completion, real tab stops, find/replace.
- **A test runner** — 39 problems ship 225 verified cases; **Random** fuzzes your code against the
  reference solution and prints the first disagreeing input; **Big-O** estimates your complexity.
- **Eleven wrong solutions were found and corrected** while building this, two of which failed their
  own published samples. `site/README.md` lists every one.
- **Every solution is executed before it is published** — against its own samples, and against an
  independent brute force on thousands of random inputs. The 15 problems added in September 2026
  were checked that way before a single explanation was written.

## Fixed in this pass (18 Sept 2026)

The Docker deployment could not start Python at all, and the cause was in the server, not in
Pyodide: `server.py` added its `Cache-Control` header *before* the status line was written, so every
`/vendor/` response — the whole ~10 MB runtime — went out malformed, with no status line and no
`Content-Type`. The loader treats that as a warning and then waits forever, which on screen is just
a spinner that never ends.

Fixed here, all five of them:

- **the header ordering** (the actual bug), now emitted from `end_headers()`;
- **`ThreadingHTTPServer` + HTTP/1.1**, so the runtime download no longer blocks every other asset;
- **a runtime preflight in `pyrun.js`** that checks status, MIME type and the WebAssembly magic
  bytes and says what is wrong instead of hanging;
- **retryable boot** — a failed start no longer poisons every later attempt, so *Run* really retries;
- **`vendor.sh` resumes interrupted downloads** (`--retry-all-errors -C -`) and refuses to ship a
  truncated runtime.

Verified in a real browser against the offline container build: runtime up in 2.6 s, 39 problems and
225 cases passing. `site/_e2e.html` is that self-test — open it any time; the container build strips
it.

## Also here: `fastprep/` — a practice app over 3,533 reported problems

A second, self-contained app in [`fastprep/practice/`](fastprep/practice/README.md), over the
offline FastPrep bank that `fastprep/fastprep.py` scrapes (3,533 problems from 355 companies,
already synced into `fastprep/fastprep.db`).

```sh
cd fastprep/practice && python3 serve.py      # http://127.0.0.1:8900
```

- **Browse** every metadata field as a filter and every sensible field as a sort, both directions:
  company, stage (OA 1,976 / phone screen / onsite), difficulty, topic, platform, employment type,
  target role, format, date windows, seen-count range, screenshots, your own progress. Full-text
  search over titles and statements.
- **Read** the rendered statement, examples, every sighting date, and the original assessment
  screenshots, fetched once from fastprep.io and cached.
- **Run** your solution against the problem's visible examples, in a **bubblewrap sandbox** with no
  network, no filesystem and hard CPU/memory/time limits. Passing is never presented as proof:
  the bank ships no hidden tests.
- **Track** attempted/solved/review, bookmarks, notes and submissions in a separate `progress.db`,
  so `fastprep.py sync` can refresh the bank without touching your work.

89 tests: `python3 serve.py --selftest`.

## Docs

- [`site/README.md`](site/README.md) — the app in detail: every feature, keybinding, and the full
  record of corrections and unresolved source contradictions.
- [`ADDING-PROBLEMS.md`](ADDING-PROBLEMS.md) — how to turn a new batch of screenshots into entries,
  including the verification step that matters most.

## Regenerating the offline bundle

`dist/` is a build artifact and is not committed. To produce a self-contained copy without Docker:

```sh
./scripts/vendor.sh dist
python3 -m http.server -d dist 8080     # http://localhost:8080/site/
```

Running under plain `http.server` has **no** `/api/state` endpoint, so state stays in the browser's
`localStorage` (per-browser, wiped with the cache). Use the Docker image for server-side persistence.
