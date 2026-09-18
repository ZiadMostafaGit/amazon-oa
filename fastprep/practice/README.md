# FastPrep practice

A local practice app over the offline FastPrep bank: browse and filter 3 533
reported interview problems, read the statement with its original screenshots,
write a solution, and run it against the problem's visible examples in a
sandbox.

```sh
python3 serve.py            # http://127.0.0.1:8900
```

That is the whole setup. No dependencies, no build step, no account, and no
network traffic except the one thing that needs it (source screenshots, below).

```sh
python3 serve.py --open              # …and open a browser
python3 serve.py --port 9000         # somewhere else
python3 serve.py --offline           # never fetch images; serve what is cached
python3 serve.py --host 0.0.0.0      # reachable from elsewhere (no auth: see below)
python3 serve.py --base-path /site   # behind a proxy that forwards its mount prefix
python3 serve.py --prefetch-images   # cache all 2 025 screenshots, then exit
python3 serve.py --image-cache DIR   # keep screenshots somewhere else (a Docker volume)
python3 serve.py --selftest          # run the 115 tests
```

## What it does

**Browse.** Every metadata field is a filter and every sensible field is a
sort, freely combined.

*Filters* — company, stage (OA / phone screen / onsite), difficulty, topic,
assessment platform, employment type, target role, practice format; a "newest
sighting" window and a "seen on any date" window; a seen-count range; has
source screenshots; and your own status, bookmarks and notes. Several values
inside one facet are OR, different facets are AND, and each facet with more
than a dozen values gets a type-to-filter box. Where a field is empty for some
problems there is an **(not set)** option with its own count — 1 557 problems
name no platform, 76 no difficulty, 523 no employment type — so nothing in the
bank is unreachable.

*Sorts* — date last seen, times seen, difficulty, title, company, bank order,
plus relevance while searching. Each is a **field plus a direction button**, so
every one reads either way (hardest→easiest or easiest→hardest, A→Z or Z→A);
press `r` to flip it. Rows whose value is unknown stay at the bottom in both
directions rather than flooding the top.

Full-text search covers titles, statements, constraints and source notes
(SQLite FTS5, built in memory at startup). The active result count sits in the
header, and the whole state lives in the URL, so any view can be bookmarked or
shared.

**Read.** Rendered statement and constraints (they are HTML in the data, and
are rendered as HTML, not dumped as tags), every example with its inputs,
expected output and explanation, topics, difficulty, company, platform, every
`lastSeen` date, the source note, and the original assessment screenshots
inline — click to enlarge. Tabular (SQL) problems have no `examples`; they get
their table schemas, result contract and visible cases rendered as tables
instead.

**Solve.** A real editor, not a textarea: CodeMirror with Python highlighting,
**Vim keybindings** (`Ctrl-Alt-V`, with the mode shown next to the button),
**relative line numbers** (`Ctrl-Alt-R`) so `5dd` and `3j` line up with the
gutter, real tab stops, Python-aware Enter and Backspace, and completion over
every builtin, all 297 stdlib modules and the methods of the built-in types.
Font size, reset-to-starter and copy sit in the same bar, and your buffer is
saved per problem and per language as you type.

Three ways to run it:

| Button | What it does |
|---|---|
| **▶ Run tests** (`Ctrl-Enter`) | the published examples plus your own cases |
| **Run my cases only** | just the cases you added, for iterating on one edge case |
| **Scratch** (`Shift-Ctrl-Enter`) | evaluate any expression against your code — `solve([1,2,3])`, `print(helper(x))` |

Each case reports pass/fail with expected versus actual and anything the code
printed.

**Generated test cases.** 1,103 of the 3,533 problems publish exactly *one*
example, which catches a misunderstanding but not an off-by-one. Where a
verified reference solution exists, `tools/cases.py` mutates that problem's own
examples — keeping their vocabulary and shape, so a list of command words stays
a list of command words — runs the reference over the variants, and stores the
pairs in `solutions/cases/<id>.json`. They run with ▶ Run tests, badged
*generated*.

They earn their place: on `amazon-stock-span`, a solution with `<` where it
needs `<=` **passes the single published example** and fails 2 of the 6
generated cases. Their expected values are the reference's behaviour, not a
judge's — which is why only verified references are used and why the app says
so wherever they appear.

**Your own test cases.** *＋ Add a test case* gives you one field per declared
parameter, pre-filled from the first example so the notation is obvious, plus an
expected value and a note. **Leave the expected value empty** and the case still
runs — it reports `RAN` and shows what your code returned, which is how you
explore an edge case you do not yet know the answer to. Cases live in
`progress.db` next to your notes, never in the bank.

**Reference solutions.** Where one exists it sits in a collapsed panel at the
bottom of the problem, badged with the verification it passed, with a button to
load it into the editor. The bank ships none of these: see *Solutions* below.

**Track.** Attempted / solved / review, bookmarks, notes and your last
submission per language, kept in `progress.db` — a separate file, because
`python3 fastprep.py sync` rewrites `fastprep.db` and would take your data with
it.

## The part to be careful about: running your code

User code is hostile by assumption. It never runs in the server process.

| Layer | What it does |
|---|---|
| **bubblewrap** (`bwrap`) | new user/pid/net/ipc/uts namespace, **no network interface**, read-only `/usr`, private tmpfs, `--clearenv`, `--new-session`. The problem bank, your home directory and this app are simply not in the filesystem it sees. |
| **rlimits** | `RLIMIT_CPU` 8 s, `RLIMIT_AS` 768 MB, `RLIMIT_NOFILE`, `RLIMIT_FSIZE` 16 MB, `RLIMIT_NPROC` 256 — soft and hard set together, so the code cannot raise them back. |
| **wall clock** | the parent kills the whole process group after 10 s. |
| **payload** | code and cases cross as a base64 blob inside the program, and the verdict comes back behind a per-run nonce, so a stray `print` is never read as a result. |
| **output** | capped at 64 000 bytes per run. |

If `bwrap` is missing the app still runs, but it says so in the header and in
the startup banner, and the isolation is then rlimits plus your OS user only.
`tests/test_runner.py` asserts the guarantees: no network, no reading the bank,
no writing outside, infinite loops stopped, memory capped.

**Passing is not proof.** This bank ships only VISIBLE examples — no hidden
tests, no reference solutions. The app says so next to every Run button, and a
clean sweep marks a problem *attempted*, never *solved*; that call is yours.

### Solutions

The bank has no reference solutions and no hidden tests, so every solution here
was written for this repo and is only kept if it passes **every visible example
of its problem**. The tooling is the point:

```sh
python3 tools/pick.py 1500        # choose the problems worth solving -> solutions/MANIFEST.json
python3 tools/brief.py <id>       # statement + constraints + exact signature + examples
python3 tools/verify.py <id>      # run a stored solution against its examples, in the sandbox
python3 tools/verify.py --all     # re-check everything -> solutions/VERIFIED.json
python3 tools/audit.py            # flag anything that passes by memorising the examples
python3 tools/cases.py            # generate extra cases from the verified references
python3 tools/gaps.py             # what every problem is missing, counted
```

`tools/pick.py` blends two rankings rather than choosing between them — most
repeated (`seen_count`) and most recent (`last_seen_max`) — because they
disagree: the most-repeated problems skew old, the newest are mostly seen once.

`tools/gaps.py` is the inventory of what the bank does not have. Every problem
has a statement and at least one example; 1,914 have no screenshots, 1,103 have
a single example, 310 have no constraints, 76 have neither topics nor
difficulty. Those gaps are shown on the problem rather than rendered as empty
sections, and the single-example gap is what `tools/cases.py` fills.

`tools/audit.py` exists because "passes the visible examples" can be gamed by
returning the expected answer for the example input. It greps every solution for
the examples' literal inputs and outputs and for equality chains with no loop,
and prints what it finds. It is a report to read, not a gate that deletes files:
a legitimate lookup table trips it too.

A solution the app shows as *verified* passed `tools/verify.py` on the date in
`solutions/VERIFIED.json`. Anything without that badge is stored but unconfirmed.

### Languages

The bank's starter code is Java (and MySQL / PostgreSQL / pandas for tabular
problems). The app probes this machine at startup and marks each language
runnable or read-only rather than pretending:

| Language | Status here | Notes |
|---|---|---|
| Python 3 | **runnable** | signature generated from `functionName` + the example types, so the runner calls exactly what you see. `ListNode` / `TreeNode` are provided. |
| SQL | **runnable** | tabular problems only: the visible cases are loaded into an in-memory SQLite database built from `inputSchema`. SQLite is close to MySQL/Postgres but not identical, and the UI says so. |
| Java | read-only unless a JDK is installed | the original starter code is shown; switch to Python to run. |
| pandas | read-only unless pandas is installed | starter code shown as published. |

### Parsing the examples

Every `inputValue` is a string with a declared type (`int[]`, `String[][]`,
`char[][]`, `List<List<String>>`, `TreeNode`, …). `parsing.py` turns those into
Python values and back. It is the piece most likely to be quietly wrong, so it
is tested two ways:

* `tests/test_parsing.py` — 31 unit tests over every type family, including the
  LeetCode tree encoding (`[1,null,2,3]`), cycles, tolerance on floats, and the
  traps (`["None"]` is the *string* None; `"1e2"` is a string, not a number).
* `tests/test_corpus.py` — parses **every example in all 3 533 problems**
  (13 566 input values, 7 214 outputs) and asserts each expected output
  compares equal to itself. This is how the one Java `long` literal in the bank
  (`9000606388L`) was found.

## Behind a reverse proxy

The page and every request it makes are resolved **relative to wherever the app
is mounted**, so it works at `/`, at `/site/`, or anywhere else. Which flag you
need depends on what your proxy does with the prefix:

```nginx
# nginx strips the prefix (note the trailing slash on proxy_pass):
location /site/ { proxy_pass http://127.0.0.1:8900/; }      # no flag needed

# nginx forwards it verbatim (no trailing slash):
location /site/ { proxy_pass http://127.0.0.1:8900; }       # --base-path /site
```

With `--base-path /site` the app answers on both `/site/...` and `/...`, so a
misconfigured proxy fails loudly rather than half-working. There is **no
authentication** and the app executes code by design: keep it on `127.0.0.1`
behind your proxy's auth, or reach it over an SSH tunnel.

## Source screenshots

1 619 problems carry 2 025 screenshots, referenced by path only — the bytes are
not in the database. The first view of a problem fetches its images from
fastprep.io and writes them to `cache/images/`; every later view is local. That
is the only outbound request the app makes, it is capped at **3 req/s**,
single-flight per image, and never repeated for a cached file. `--offline`
disables it; `--prefetch-images` warms the whole cache in about 11 minutes.

## Layout

```
serve.py       one-command entry point + HTTP API (stdlib only)
solutions.py   the reference-solution store and its verification state
fpdb.py        read-only access to fastprep.db, filters, sorts, FTS search
parsing.py     inputValue/outputText <-> Python values, and the comparator
runner.py      the sandbox: bubblewrap + rlimits + timeout
harness_*.py   what runs inside it (python cases, SQL cases, scratch)
languages.py   what this machine can actually execute, and the starter code
progress.py    your status/notes/bookmarks/submissions (separate db)
images.py      lazy, rate-limited screenshot cache
static/        the page: index.html, app.js, styles.css, editor.js (CodeMirror + vim), pyenv.js
tests/         115 tests: parsing, corpus sweep, sandbox, API, filters/sorts,
               custom cases, scratch, solutions, random mode, generated cases
tools/         pick / brief / verify / audit / batch — the solution pipeline
solutions/     one file per problem id, plus MANIFEST.json and VERIFIED.json
static/vendor/ CodeMirror and JetBrains Mono, vendored so the app is fully offline
```

## Notes on the data

* Stage lives in `problem_types`, a **JSON array stored as TEXT**, and is
  queried with `json_each`. The singular `problemType` in `detail_json` is null
  for 1 082 of 3 533 rows; filtering on it silently loses a third of the bank.
  The OA filter here returns **1 976**.
* `detail_json` is the truth when a flat column disagrees with it.
* `problemStatement`, `constraints` and `explanation` are HTML.
* Recency is `last_seen_max`; repetition is `seen_count`; `last_seen` is the
  full array of sightings, and the problem view lists every one.
* 3 485 problems are `algorithm` (examples + Java starter code), 48 are
  `tabular` (no examples; `inputSchema`, `visibleCases`, `resultContract`).

The bank is opened `file:…?mode=ro` everywhere. Re-running
`python3 fastprep.py sync` refreshes it under the app with no conflict, and
your progress is untouched.
