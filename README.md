# Amazon OA practice

41 Amazon / Siemens online-assessment problems transcribed from screenshots, each with a worked
solution and a step-by-step derivation, plus a Python editor and a test runner that executes real
CPython **in the browser**. No backend, no build step, no account.

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

**In Docker** — self-contained, works with no internet at all:

```sh
docker compose up --build -d      # then open http://localhost:8080
```

or without compose:

```sh
docker build -t amazon-oa-practice .
docker run -d -p 8080:80 --name amazon-oa amazon-oa-practice
```

The build fetches CodeMirror, the font and the Pyodide runtime into the image and rewrites the two
files that reference them, so the container never reaches the network at run time.

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
docker run -d -p 8080:80 YOURNAME/amazon-oa-practice
```

## What's in the app

- **41 problems** — 15 Amazon coding, 2 work simulation, 6 debugging projects, 5 Siemens,
  12 FastPrep, plus a frame-by-frame post-mortem of a real 60-minute attempt.
- **37 answer sets** — Hint 1 → Hint 2 → Solution → *Step by step*, the last deriving every formula
  and tracing the published sample numerically to its stated answer.
- **A Python editor** — Vim mode, stdlib-wide completion, real tab stops, find/replace.
- **A test runner** — 24 problems ship 126 verified cases; **Random** fuzzes your code against the
  reference solution and prints the first disagreeing input; **Big-O** estimates your complexity.
- **Eleven wrong solutions were found and corrected** while building this, two of which failed their
  own published samples. `site/README.md` lists every one.

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
