# Build a practice app over the FastPrep problem database

## What exists already
A fully populated SQLite database at `fastprep.db` in this directory
(17 MB, 3533 problems, 100% complete — no fetching needed, work offline).
`fastprep.py` in the same dir is the scraper + CLI that produced it. Read it
first; reuse its `html_to_text()` and `render_markdown()` rather than rewriting.

Inspect the data before designing:

    python3 fastprep.py sql            # read-only SQL console (.schema / .cols)
    python3 fastprep.py schema         # detail_json shape, algorithm problems
    python3 fastprep.py schema --format tabular
    python3 fastprep.py stats

## Ground truth — verify these yourself, don't assume
- Table `problems`, one row per problem. Flat columns for querying, PLUS
  `detail_json` holding the complete original API payload. When a column and
  detail_json disagree, detail_json is the truth.
- `problem_types`, `topics`, `employment_types`, `target_roles`, `last_seen`
  are **JSON arrays stored as TEXT**. Query with json_each(), e.g.

      WHERE EXISTS (SELECT 1 FROM json_each(problem_types) WHERE value='OA')

- Filter stage on `problem_types` (array), NEVER `problem_type` (singular) —
  the singular is NULL for 1082 of 3533 rows and will silently drop a third
  of the bank.
- `problemStatement`, `constraints`, `explanation` are **HTML** strings.
- Recency: `last_seen_max` (newest sighting). Repetition: `seen_count`.
  `last_seen` is the full array of every date the problem was reported.
- TWO problem shapes, handle both explicitly:
  * practice_format='algorithm' (3485): `examples[]`, Java-only `starterCode`,
    `functionName`.
  * practice_format='tabular' (48): NO `examples`. Instead `tabular` with
    `inputSchema`, `visibleCases`, `resultContract`, and `languages[]`
    (mysql / postgresql / pandas, each with its own starterCode).
- `sourceImages[]` (1619 problems, 2025 images) are path strings like
  `/api/problem-source-images/<problem-id>/0` — screenshots of the real
  assessment. Check whether they have been downloaded locally; if not, serve
  them from https://www.fastprep.io + path, and cache locally on first use.
- ALL examples are exampleType='VISIBLE'. There are NO hidden tests and NO
  reference solutions in this data.

## Build
A local app (your choice of stack — justify it briefly; a local web app is the
obvious fit since statements are HTML and there are images to render).

1. **Browse / sort / filter over everything.** Every metadata field must be
   filterable and every sensible field sortable, combinable, in any order:
   company, stage (OA / phone screen / onsite), difficulty, topic,
   assessment platform, employment type (INTERN / NEW GRAD / FULLTIME),
   target role, practice format, date-seen ranges. Sorts must include
   most-recent (`last_seen_max`) and most-frequently-seen (`seen_count`).
   Full-text search across title and statement. Show the active result count.
2. **Problem view.** Rendered statement + constraints (render the HTML, don't
   dump tags), examples with inputs/expected output/explanation, topics,
   difficulty, company, every `lastSeen` date, `sourceNote`, and — when
   present — the source screenshots displayed inline, full-size on click.
   Handle the tabular shape with its table schemas instead of examples.
3. **Code editor + test runner.** Load `starterCode`, let the user run against
   the visible examples, show per-case pass/fail with expected vs actual.
   - Parse `inputValue` strings according to `inputType` (int[], int[][],
     String, List<String>, ...). Write this parser carefully and unit-test it;
     it is the part most likely to be quietly wrong.
   - Starter code is Java. If you support other languages, generate the
     signature from `functionName` + the example types — do not pretend a
     language is supported when you cannot actually execute it.
   - **Execute untrusted user code in a sandbox** (container, subprocess with
     resource/time limits, or a WASM runtime). Enforce a timeout. Never
     eval user code in the app process.
   - For tabular problems, run SQL against an in-memory DB built from
     `inputSchema` + `visibleCases`.
   - The UI must state that these are visible examples only and that passing
     them does NOT mean the solution is correct. Do not show a message
     implying full verification.
4. **Progress tracking** in a SEPARATE table or db file (attempted / solved /
   bookmarked / notes / last submission). Do not write to the `problems`
   table — re-running `python3 fastprep.py sync` refreshes it and would wipe
   your data.

## Constraints
- Open the problems db **read-only** (`file:...?mode=ro`) everywhere except
  your own progress store.
- Do not re-scrape fastprep.io. The data is already local and complete. The
  only acceptable network calls are lazily fetching source images not yet
  cached, rate-limited to ~3 req/s.
- Keep it runnable with one command and document it in a README.

## Verify before claiming done
Actually run it and confirm with real data, reporting the numbers:
- OA filter returns 1976 problems; sorting by recent puts 2026-09-18 first.
- A problem WITH images renders them (e.g. adobe-determine-edit-distance-in-word-ladder).
- A tabular problem renders correctly (practice_format='tabular').
- A known-correct solution passes all visible cases on a multi-input problem
  such as `stripe-deployment-window-scheduler` (hard, 2 parts, String[] input).
- A deliberately wrong solution reports failures rather than passing.

State clearly anything you did not finish.
