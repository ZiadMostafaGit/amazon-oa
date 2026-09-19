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

*Filters* — has a reference solution, company, stage (OA / phone screen / onsite), difficulty, topic,
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

**Study.** Press `s` or the **Study** button for the other half of the app: a
canon of **150 topics**, ranked by how many of these 3 533 problems actually use
them. Each one opens a chapter written to a fixed outline — when you reach for
it, the idea, a worked-by-hand trace, *why it is correct* (a real invariant /
base case / inductive step / termination argument, not a restatement), a derived
complexity, a clean implementation, the variants, how to recognise it in a
statement, the traps, and what to memorise — followed by self-check questions
whose answers stay hidden until you ask.

Inside a chapter the code blocks are **live**: edit them in place and press Run,
and they execute in the same sandbox as your solutions. Diagrams are inline SVG.
Every chapter ends with a **practice queue** — the problems in this bank that
drill that topic, easiest first, marked with what you have already solved — and
your reading state, notes and edits are saved server-side like everything else.
The topic chips under a problem statement jump straight to the matching chapter.

Topics are mapped to problems by the bank's own tags **plus** keyword patterns
over the statements, because the bank tags only 36 coarse subjects and "stack"
cannot tell you a problem wants a monotonic stack. A topic that no problem here
uses is **kept and marked rare** rather than dropped: it is still worth knowing,
and saying "nothing in this collection uses it" is more useful than silence.

**The layout.** Two panes: the problem on the left, the editor on the right,
with **draggable dividers** — one between the panes, one between the editor and
its output. Both remember where you left them, and double-click resets either.
The editor pane is a flex column that never scrolls as a whole, so the toolbar
is pinned above the code and **Run, Random, Scratch and the verdict are always
on screen** — no scrolling past the statement to reach them. Drag the divider
to change the split; it is remembered. Browsing lives in a drawer (`/` or the
Problems button), which gives the filters real room instead of a cramped third
column.

**Solve.** A real editor, not a textarea: CodeMirror with Python highlighting,
**Vim keybindings** (`Ctrl-Alt-V`, with the mode shown next to the button),
**relative line numbers** (`Ctrl-Alt-R`) so `5dd` and `3j` line up with the
gutter, real tab stops, Python-aware Enter and Backspace, and completion over
every builtin, all 297 stdlib modules and the methods of the built-in types.
Font size, reset-to-starter and copy sit in the same bar, and your buffer is
saved per problem and per language as you type.

**Completion that stays out of the way.** It opens after a dot, and from the
*second* letter of a word — one letter matches a few thousand names, which is a
list, not a suggestion. `Tab` takes the highlighted entry; **`Enter` does not**
— it closes the list and makes the newline you asked for, which in Python is
also the indent. Prefixes ignore case, so `coun` reaches `Counter`. What it
offers is typed from the buffer: `d = {}` completes dict methods (`{}` is an
empty dict — the empty set is `set()`), `q = deque()` completes `popleft`, a
`nums: List[int]` annotation completes list methods before you have written a
line, `self.` completes the attributes you assigned, and `collections.` lists
that module's own members rather than a generic pile of method names.

**Room for the code.** The editor keeps the pane: the per-language note (the
same sentence on every Python problem) hides behind an **ⓘ** in the toolbar,
and the output panel appears when there is output and gives its third of the
pane back when you dismiss it with **✕**.

Four ways to run it:

| Button | What it does |
|---|---|
| **▶ Run tests** (`Ctrl-Enter`) | the published examples plus your own cases |
| **▶ Run code** (`Alt-Enter`) | just runs it, like `python file.py`, and shows everything it printed — no cases, no expression to invent. `__name__` is `"__main__"` here, so a main block runs; under the test harness it deliberately does not |
| **Run my cases only** | just the cases you added, for iterating on one edge case |
| **Scratch** (`Shift-Ctrl-Enter`) | evaluate any expression against your code — `solve([1,2,3])`, `print(helper(x))` |
| **Solution** | the reference solution for this problem, with its verification badge and a button to load it into the editor — or, when there is none, which problems do have one |

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

**Nothing is lost.** Your code (per problem and per language), your notes and
your test cases are server-side state, saved as you type and confirmed by a
badge in the header. The editor is never rebuilt from the server copy while it
holds something newer: what was last in the buffer for this problem *and* this
language wins, so adding a test case, deleting one, or flipping to the Java tab
and back cannot hand you the version from when you opened the problem. What
gets saved is captured *when you type*, not when the debounce fires — otherwise switching problems mid-debounce writes your code
onto the problem you just left — and anything still pending is flushed with
`sendBeacon` when the page is hidden or closed. Close the tab, reopen it a week
later, and the buffer is where you left it.

**Race the clock.** Press `t` or the **Timer** button in the header. Pick 15, 20,
30, 45, 60 or 90 minutes, or type a length — `45` is minutes, `12:30` is a
clock, `1:30:00` has hours in it, `90s` and `2h` say which unit they mean. The
button becomes the countdown, a hairline under the header drains with it, and
the colour turns amber under five minutes and red under one. Pause, resume,
`+5 min` and reset are all in the panel; *Start a fresh clock whenever I open a
problem* turns every problem you open into a timed attempt at your last length.

When it runs out the page says so and *sounds* it: three rising beeps from a
few oscillators — no audio file to ship — repeated for half a minute, the tab
title flashing **⏰ Time is up** until you acknowledge it, a desktop
notification if you asked for one, and a card offering `+5 minutes`, *Run it
again* or *Done*. Nothing is submitted and nothing is discarded; the clock just
stops.

The clock is a **deadline, not a counter**: every tick reads the wall clock and
subtracts, and the deadline itself is what gets stored. So a background tab
that stops getting timers, a laptop that slept, and a reload mid-attempt all
leave you with exactly the time you had — and if a run expires while the tab is
closed, reopening it says so without the beeping. This is the one piece of your
state that lives in `localStorage` rather than `progress.db`: it is a clock on
*this* screen, not a fact about a problem.

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

### When the machine will not allow all of that

`bwrap` being installed says nothing about whether this kernel, container or
systemd unit will let it build namespaces. On some machines it makes every
namespace except the network one and dies before your code starts:

```
bwrap: loopback: Failed RTM_NEWADDR: Operation not permitted
```

There, a full sandbox is not a stricter option — it is a broken one, and every
single run fails. So the runner **works out what this machine allows by running
bwrap once**, and settles for the best tier that actually works:

| Tier | Badge | What you give up |
|---|---|---|
| `bubblewrap` | `sandboxed` | nothing |
| `bubblewrap-shared-net` | `sandboxed · shared network` | the network namespace only: your code can reach whatever this host can reach. Filesystem, pids and ipc are still isolated. |
| `subprocess` | `limited sandbox` | every namespace: rlimits and your OS user are all that is left. |

The tier is named in the startup banner, in the header badge (amber for the
lower two, with the reason in its tooltip), in `/api/health`, and on every run
— so if a sandbox stops working while the app is up, the runner re-checks,
keeps running your code at the tier that works, and the badge changes to match.
A failure that does happen is reported as *the sandbox could not start*, never
as your code raising: bwrap dying is not your bug.

`tests/test_runner.py` asserts the guarantees — no network, no reading the
bank, no writing outside, infinite loops stopped, memory capped — and, with a
fake `bwrap` that fails the way the real one does, that each tier is found and
that a dead sandbox is never blamed on the code in the editor.

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

**Where it stands.** 1,484 of the 1,500 targeted problems have a reference
solution, and every one of them was re-verified in a single pass after the fact
(18 s at `--jobs 10`), not merely trusted from whoever wrote it. 1,403 of those
carry generated cases — 8,411 in total. `tools/audit.py` flags 48 solutions;
reading them, 44 are a problem's own required sentinel (`"INVALID"`, `"-1"`,
`["None"]`) and 4 are branch-heavy closed forms (the knight-distance formula
with its two known exceptions, factorial counting, list slicing). None is a
memorised answer — which is the point of reading the report rather than
trusting the count.

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

**You usually need neither flag.** The app works out where it is mounted on its
own: it honours `X-Forwarded-Prefix` if the proxy sets it, and otherwise treats
any leading path segments that are not its own routes (`api`, `app.js`,
`vendor`, …) as a mount prefix. `--base-path` only exists to pin that down
explicitly. A typo under the mount point still 404s rather than silently
serving the app, and `/site` redirects to `/site/` so the page's relative URLs
resolve inside the mount point.

A ready-made location block for an nginx that already proxies other apps on the
same domain is in [`deploy/nginx-site.conf`](../../deploy/nginx-site.conf). There is **no
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
harness_*.py   what runs inside it (python cases, SQL cases, scratch, plain run)
languages.py   what this machine can actually execute, and the starter code
progress.py    your status/notes/bookmarks/submissions (separate db)
images.py      lazy, rate-limited screenshot cache
topics.py      the study space: the canon, its articles, and each topic's queue
mdlite.py      the small strict Markdown dialect the chapters are written in
static/        the page: index.html, app.js, study.js, timer.js, styles.css,
               editor.js, pyenv.js
tests/         192 tests: parsing, corpus sweep, sandbox and its fallbacks,
               API, filters/sorts,
               custom cases, scratch, running as a script, solutions, random
               mode, generated cases, the canon, the topic mapping, the
               renderer, the study endpoints, and the page's own wiring
tools/         pick / brief / verify / audit / batch — the solution pipeline
               canon / topicmap / brief_topic / verify_topic — the study space
solutions/     one file per problem id, plus MANIFEST.json and VERIFIED.json
topics/        CANON in tools/canon.py, INDEX.json (generated), AUTHORING.md,
               and articles/<slug>.md — one chapter per topic
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
