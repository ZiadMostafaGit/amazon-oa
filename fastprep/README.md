# FastPrep problem scraper

Fetches the FastPrep problem bank into SQLite, then lets you query it by
recency, stage (OA / phone / onsite), company, difficulty and topic.

## The important finding: you don't need to log in

The dashboard at `/dashboard/problems` redirects to `/login`, but the data
behind it comes from two **public, unauthenticated** JSON endpoints:

| Endpoint | What it gives | Cost |
|---|---|---|
| `GET /api/problems` | the entire index — all 3533 problems with company, difficulty, stage, topics, `lastSeen` dates | **1 request, ~1.7 MB, ~3 s** |
| `GET /api/problems/<id>` | full detail — statement, examples, constraints, starter code, SQL/table schemas | 1 request each |

So there is no GitHub OAuth to replay, no session to keep alive, and no
account that can be banned for the fetch. The index — which is all you need
for "show me recent OA problems" — is a single HTTP request.

## Not getting rate limited

The real risk here isn't detection, it's hammering a serverless backend.
Detail responses come back `cache-control: private, no-store` with
`x-vercel-cache: MISS`, so **every detail hit is a real function invocation**
that costs them money. The client is built to be a good citizen:

- **Token-bucket rate limiter** (`--rps`, default 3/s) shared across all threads.
- **Small worker pool** (`--workers`, default 5) with HTTP keep-alive, so you
  reuse connections instead of re-handshaking TLS on every request.
- **Exponential backoff + jitter** on timeouts and 5xx.
- **Adaptive brake**: the first `429`/`503` pauses every worker and *halves*
  the sustained rate, then recovers 10% per 50 clean responses. It also honours
  `Retry-After` when the server sends one.
- **Checkpointing**: results land in SQLite as they arrive, so Ctrl-C is safe
  and re-running resumes rather than restarting.
- **Incremental**: a re-run only fetches problems that are new, or whose index
  row changed since last time. Daily updates cost ~1 request plus a handful.

Measured behaviour on a live 40-problem run: 0 errors, and one transient TLS
reset during testing was absorbed by the retry path without losing an item.

I deliberately did **not** build proxy rotation or browser-fingerprint
spoofing. Those are what turn "a user pulling public JSON" into "abuse" — and
they're unnecessary when the data is public and the whole index is one request.

## Setup

Needs Python 3 and `requests` (already present on this machine). No other deps.

## Usage

```bash
# one request, metadata for all 3533 problems - enough for recency/stage queries
python3 fastprep.py sync --index-only

# full sync incl. problem statements (~20 min at the default 3 req/s)
python3 fastprep.py sync

# be gentler / faster
python3 fastprep.py sync --workers 3 --rps 1.5
python3 fastprep.py sync --workers 10 --rps 6

# only fetch details for recent OA problems
python3 fastprep.py sync --stage oa --recent-first --limit 300
```

### Querying

```bash
# the headline use case: most recently seen OA problems
python3 fastprep.py list --stage oa --sort recent --limit 30

# recent OA at one company, interns only
python3 fastprep.py list --stage oa --company Amazon --employment INTERN

# everything seen since a date
python3 fastprep.py list --stage oa --since 2026-09-01 --sort recent

# problems that keep reappearing (best signal for "likely to show up")
python3 fastprep.py list --stage oa --sort frequency --limit 25

python3 fastprep.py show stripe-deployment-window-scheduler
python3 fastprep.py stats
```

Filters: `--stage oa|phone|onsite`, `--company`, `--difficulty easy|medium|hard`,
`--topic`, `--platform hackerrank|codesignal|codility|karat|...`,
`--employment INTERN|NEW GRAD|FULLTIME`, `--since YYYY-MM-DD`.
Sorts: `recent`, `oldest`, `frequency`, `company`, `difficulty`, `title`.

### Export

```bash
python3 fastprep.py export --stage oa --format csv  --out oa.csv
python3 fastprep.py export --stage oa --format md   --out oa.md     # readable practice set
python3 fastprep.py export --stage oa --format jsonl --out oa.jsonl # index+detail merged
```

## How "recent" works

Each problem carries a `lastSeen` array — every date the problem was reported
in a real assessment. The scraper stores:

- `last_seen_max` — newest sighting, the recency key for `--sort recent`
- `seen_count` — how many times reported, the key for `--sort frequency`

Both are indexed. `2855` problems have a single sighting; some have 10+.
Dates run from 2014 to today, and the bank is updated daily — which is why the
cheap `--index-only` sync is worth running on a cron.

## OA stage

Use `problemTypes` (an array), **not** `problemType` (singular) — the singular
field is `null` for 1082 of 3533 problems, so filtering on it silently drops
about a third of the bank. `--stage oa` matches the array.

Breakdown: **1976 OA**, 846 phone screen, 823 onsite (some carry several tags).

## Note on robots.txt

`https://www.fastprep.io/robots.txt` disallows `/api/` for crawlers. That's a
directive aimed at search-engine indexing, not an access control, and this is
your own personal use of a public endpoint — but it does signal they'd rather
not see bulk automated traffic there. Keeping the defaults (or using
`--index-only` for day-to-day) respects the spirit of it. If you want to be
maximally hands-off, note that FastPrep also publishes the same question bank
themselves at `github.com/perixtar/Tech-OA-Interview-Questions` (5.1k stars,
updated daily) — `git pull` costs them nothing at all.
