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
ad-hoc calls against your code. Or just **▶ Run code** (`Alt-Enter`): it executes the buffer the
way `python file.py` would and shows everything it printed — the button you want when you have
put a `print` in a loop to see what it is doing.

**Never in the app's process.** Your code runs under bubblewrap in a new user/pid/net/ipc
namespace with no network interface, a read-only `/usr`, a private tmpfs, hard CPU/memory/file
limits, and a wall-clock kill. What a machine *allows* is not what a machine *has*: the runner
starts bwrap once to find out, and where a full sandbox cannot be built it drops to the best one
that can — sharing the host's network, or rlimits alone — and says which in the header, rather
than failing every run. `bwrap` dying is reported as the sandbox failing, never as your code.

**Reference solutions.** The bank ships none, so **1,484** were written here — for the most
repeated and most recent problems — and each is kept only if it passes every visible example of
its problem. `tools/verify.py --all` is the gate and re-checks all of them in 18 seconds;
`tools/audit.py` greps every solution for the examples' literal values to catch anything that
"passes" by memorising them.

**More cases than the bank ships.** 1,103 problems publish exactly one example, which catches a
misunderstanding but not an off-by-one. Where a verified solution exists, the app mutates that
problem's own examples and answers them with the reference: **8,411 generated cases across 1,403
problems**. On `amazon-stock-span`, a solution with `<` instead of `<=` passes the single
published example and fails 2 of its 6 generated cases.

**Race the clock.** Press `t` and pick a length — a preset, or `45` / `12:30` /
`1:30:00` / `90s`. The header button becomes the countdown and a hairline drains
under it; when it runs out the page beeps, flashes the tab title and says so.
The deadline is what is stored, not a counter, so sleeping, a background tab or
a reload cannot quietly hand you more time.

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
