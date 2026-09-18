# FastPrep practice

Browse, filter and solve **3,533 reported interview problems** offline — every one of them
scraped from FastPrep into `fastprep/fastprep.db`, rendered with its original assessment
screenshots, and runnable against its published examples in a sandbox.

```sh
cd fastprep/practice && python3 serve.py       # http://127.0.0.1:8900
```

No dependencies, no build step, no account. Python 3 and a browser.

```sh
docker compose up --build -d                   # http://localhost:8900
```

## What it does

**Browse.** Every metadata field filters and every sortable field reads in either direction:
company (355 of them), stage (OA 1,976 / phone screen 846 / onsite 823), difficulty, topic,
assessment platform, employment type, target role, practice format, date windows, a seen-count
range, has-screenshots, plus your own status, bookmarks and notes. Full-text search over titles,
statements, constraints and source notes. Fields that are empty for some problems get an
**(not set)** bucket, so nothing in the bank is unreachable.

**Read.** The statement and constraints rendered as HTML (they are HTML in the data), every
example with inputs, expected output and explanation, every date the problem was reported, the
source note, and the original assessment screenshots inline — 2,025 of them across 1,619
problems, fetched once from fastprep.io at ≤3 req/s and cached. Tabular (SQL) problems render
their table schemas, result contract and visible cases instead.

**Solve.** A real editor — CodeMirror with Python syntax, **Vim keybindings**, **relative line
numbers**, real tab stops, Python-aware Enter/Backspace, and completion over the whole standard
library. Run against the published examples, add **your own test cases** (with or without an
expected value — one without just shows you what your code returned), and a **scratch pad** for
ad-hoc calls against your code.

**Never in the app's process.** Your code runs under bubblewrap in a new user/pid/net/ipc
namespace with no network interface, a read-only `/usr`, a private tmpfs, hard CPU/memory/file
limits, and a wall-clock kill. Without `bwrap` the app still runs and says so, loudly.

**Reference solutions.** The bank ships none, so they were written here and each one is kept only
if it passes every visible example of its problem — `python3 tools/verify.py --all` is the gate,
and `tools/audit.py` greps every solution for the examples' literal inputs and outputs to catch
anything that "passes" by memorising them.

**Track.** Attempted / solved / review, bookmarks, notes, your last submission per language and
your custom cases, all in `progress.db` — a separate file, so `python3 fastprep.py sync` can
refresh the bank without touching your work.

> **Passing is not proof.** This bank has only VISIBLE examples: no hidden tests, no official
> solutions. The app says so next to every Run button, and a clean sweep marks a problem
> *attempted*, never *solved*.

## Layout

```
fastprep/
  fastprep.py        the scraper that produced the bank (re-run: python3 fastprep.py sync)
  fastprep.db        3,533 problems, synced 2026-09-18 — opened read-only by the app
  practice/          the app: serve.py, fpdb.py, parsing.py, runner.py, static/, tools/, tests/
  practice/solutions/ reference solutions, one file per problem id
docs/                write-ups that are not in the bank and not reproducible:
                     a frame-by-frame post-mortem of a real 60-minute attempt, five debugging
                     projects, the Siemens set, the work-simulation half, field notes
video/               OCR transcripts of the recording the post-mortem was built from
```

## Docs

- [`fastprep/practice/README.md`](fastprep/practice/README.md) — the app in detail: the sandbox,
  the example parser, the solution store, every flag.
- [`docs/`](docs/) — the kept write-ups.

## History

This repo previously held a hand-built practice app over 56 problems transcribed from
screenshots. It was replaced by the FastPrep bank, which covers the same ground 60× over with
real metadata. The transcribed problems are gone; the write-ups around them are in `docs/`, and
everything is still in git history (`git log -- site/`).
