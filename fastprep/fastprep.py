#!/usr/bin/env python3
"""
fastprep.py - fetch and query the FastPrep problem bank.

Data source (both endpoints are public, no login required):
    GET /api/problems         -> index of every problem (~1.7 MB, one request)
    GET /api/problems/<id>    -> full detail: statement, examples, constraints,
                                 starter code, tabular schemas

Design notes:
  * The index is ONE request. Only the per-problem details are parallelised.
  * Every detail response is `cache-control: private, no-store` and misses the
    Vercel edge cache, so each hit is a real serverless invocation. The client
    is deliberately gentle: token-bucket rate limit, small worker pool,
    exponential backoff with jitter, Retry-After support, and an adaptive brake
    that halves throughput on the first 429 and recovers slowly.
  * Work is checkpointed in SQLite, so an interrupted run resumes for free and
    a re-run only fetches what is new or changed.

Usage:
    python3 fastprep.py sync                     # full sync (index + details)
    python3 fastprep.py sync --index-only        # just the index, 1 request
    python3 fastprep.py list --stage oa --limit 25
    python3 fastprep.py show <problem-id>
    python3 fastprep.py export --stage oa --format md --out oa.md
    python3 fastprep.py stats
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import random
import re
import sqlite3
import sys
import threading
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone

import requests
from requests.adapters import HTTPAdapter

BASE = "https://www.fastprep.io"
INDEX_URL = f"{BASE}/api/problems"
DETAIL_URL = f"{BASE}/api/problems/{{id}}"

DEFAULT_DB = os.path.join(os.path.dirname(os.path.abspath(__file__)), "fastprep.db")

# A normal browser UA: this is the site's own public JSON API and that is what
# it expects. Override with --user-agent if you prefer to identify differently.
DEFAULT_UA = (
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36"
)

STAGE_ALIASES = {
    "oa": "OA",
    "online-assessment": "OA",
    "phone": "PHONE SCREEN",
    "phone-screen": "PHONE SCREEN",
    "onsite": "ONSITE INTERVIEW",
    "interview": "ONSITE INTERVIEW",
}


def log(msg: str) -> None:
    print(f"[{datetime.now():%H:%M:%S}] {msg}", file=sys.stderr, flush=True)


# --------------------------------------------------------------------------
# throttling
# --------------------------------------------------------------------------
class Throttle:
    """Thread-safe token bucket with an adaptive brake.

    Every worker calls acquire() before a request. On a 429/503 the whole pool
    pauses and the sustained rate is halved; it recovers gradually so a single
    blip does not permanently cripple the run.
    """

    def __init__(self, rps: float, burst: float = 2.0, min_rps: float = 0.4):
        self._lock = threading.Lock()
        self._rps = float(rps)
        self._base_rps = float(rps)
        self._min_rps = float(min_rps)
        self._burst = max(1.0, burst)
        self._tokens = self._burst
        self._updated = time.monotonic()
        self._pause_until = 0.0
        self._ok_streak = 0

    def acquire(self) -> None:
        while True:
            with self._lock:
                now = time.monotonic()
                wait = self._pause_until - now
                if wait <= 0:
                    elapsed = now - self._updated
                    self._updated = now
                    self._tokens = min(self._burst, self._tokens + elapsed * self._rps)
                    if self._tokens >= 1.0:
                        self._tokens -= 1.0
                        return
                    wait = (1.0 - self._tokens) / self._rps
            # small jitter so workers do not march in lockstep
            time.sleep(max(0.005, wait) + random.uniform(0, 0.05))

    def penalise(self, pause_s: float) -> None:
        with self._lock:
            self._ok_streak = 0
            self._pause_until = max(self._pause_until, time.monotonic() + pause_s)
            self._rps = max(self._min_rps, self._rps / 2.0)
            log(f"  throttling back -> {self._rps:.2f} req/s, pausing {pause_s:.1f}s")

    def reward(self) -> None:
        with self._lock:
            self._ok_streak += 1
            if self._ok_streak >= 50 and self._rps < self._base_rps:
                self._rps = min(self._base_rps, self._rps * 1.1)
                self._ok_streak = 0

    @property
    def rps(self) -> float:
        with self._lock:
            return self._rps


# --------------------------------------------------------------------------
# http
# --------------------------------------------------------------------------
class Client:
    def __init__(self, throttle: Throttle, workers: int, ua: str,
                 cookie: str | None, timeout: float, max_retries: int):
        self.throttle = throttle
        self.timeout = timeout
        self.max_retries = max_retries
        self.session = requests.Session()
        # keep-alive pool sized to the worker count: fewer TCP/TLS handshakes
        adapter = HTTPAdapter(pool_connections=workers, pool_maxsize=workers,
                              max_retries=0)
        self.session.mount("https://", adapter)
        self.session.headers.update({
            "User-Agent": ua,
            "Accept": "application/json, text/plain, */*",
            "Accept-Language": "en-US,en;q=0.9",
            "Referer": f"{BASE}/problems",
            "Connection": "keep-alive",
        })
        if cookie:
            self.session.headers["Cookie"] = cookie

    def get_json(self, url: str):
        """GET with backoff. Returns parsed JSON, or None for a hard 404."""
        last_err = None
        for attempt in range(self.max_retries):
            self.throttle.acquire()
            try:
                r = self.session.get(url, timeout=self.timeout)
            except requests.RequestException as e:
                last_err = e
                self._backoff(attempt)
                continue

            if r.status_code == 200:
                self.throttle.reward()
                try:
                    return r.json()
                except ValueError as e:
                    last_err = e
                    self._backoff(attempt)
                    continue

            if r.status_code == 404:
                return None

            if r.status_code in (429, 503):
                retry_after = r.headers.get("Retry-After")
                pause = self._parse_retry_after(retry_after)
                if pause is None:
                    pause = min(60.0, 2.0 * (2 ** attempt)) + random.uniform(0, 1.5)
                self.throttle.penalise(pause)
                last_err = f"HTTP {r.status_code}"
                continue

            if 500 <= r.status_code < 600:
                last_err = f"HTTP {r.status_code}"
                self._backoff(attempt)
                continue

            # 401/403 and friends: retrying will not help
            raise RuntimeError(f"HTTP {r.status_code} for {url}: {r.text[:200]}")

        raise RuntimeError(f"giving up on {url} after {self.max_retries} attempts: {last_err}")

    def _backoff(self, attempt: int) -> None:
        time.sleep(min(45.0, 1.5 * (2 ** attempt)) + random.uniform(0, 1.0))

    @staticmethod
    def _parse_retry_after(value):
        if not value:
            return None
        try:
            return float(value)
        except (TypeError, ValueError):
            return None


# --------------------------------------------------------------------------
# storage
# --------------------------------------------------------------------------
SCHEMA = """
CREATE TABLE IF NOT EXISTS problems (
    id                  TEXT PRIMARY KEY,
    title               TEXT,
    company             TEXT,
    company_id          TEXT,
    status              TEXT,
    difficulty          TEXT,
    problem_types       TEXT,   -- json array: OA / PHONE SCREEN / ONSITE INTERVIEW
    employment_types    TEXT,   -- json array
    topics              TEXT,   -- json array
    target_roles        TEXT,   -- json array
    assessment_platform TEXT,
    practice_format     TEXT,
    last_seen           TEXT,   -- json array of dates
    last_seen_max       TEXT,   -- newest sighting -> the recency key
    last_seen_min       TEXT,
    seen_count          INTEGER,
    order_idx           INTEGER,
    index_hash          TEXT,   -- detects index-side changes between syncs
    index_json          TEXT,
    detail_json         TEXT,
    detail_fetched_at   TEXT,
    first_indexed_at    TEXT,
    updated_at          TEXT
);
CREATE INDEX IF NOT EXISTS idx_last_seen  ON problems(last_seen_max DESC);
CREATE INDEX IF NOT EXISTS idx_company    ON problems(company);
CREATE INDEX IF NOT EXISTS idx_difficulty ON problems(difficulty);
CREATE TABLE IF NOT EXISTS sync_runs (
    started_at TEXT, finished_at TEXT, indexed INTEGER,
    details_fetched INTEGER, errors INTEGER, note TEXT
);
"""


def connect(path: str) -> sqlite3.Connection:
    conn = sqlite3.connect(path, timeout=30, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA synchronous=NORMAL")
    conn.executescript(SCHEMA)
    return conn


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def _j(v):
    return json.dumps(v, ensure_ascii=False, sort_keys=True)


def upsert_index(conn: sqlite3.Connection, records: list[dict]) -> tuple[int, int]:
    """Insert/update index rows. Returns (new, changed)."""
    existing = {r["id"]: r["index_hash"] for r in conn.execute(
        "SELECT id, index_hash FROM problems")}
    ts = now_iso()
    new = changed = 0
    rows = []
    for p in records:
        pid = p.get("id")
        if not pid:
            continue
        blob = _j(p)
        h = hashlib.sha256(blob.encode()).hexdigest()
        prev = existing.get(pid)
        if prev == h:
            continue
        if prev is None:
            new += 1
        else:
            changed += 1
        seen = [d for d in (p.get("lastSeen") or []) if d]
        rows.append((
            pid, p.get("title"), p.get("company"), p.get("companyId"),
            p.get("status"), p.get("difficulty"),
            _j(p.get("problemTypes") or []), _j(p.get("employmentTypes") or []),
            _j(p.get("topics") or []), _j(p.get("targetRoles") or []),
            p.get("assessmentPlatform"), p.get("practiceFormat"),
            _j(seen), max(seen) if seen else None, min(seen) if seen else None,
            len(seen), p.get("order"), h, blob, ts, ts,
        ))
    conn.executemany("""
        INSERT INTO problems (
            id,title,company,company_id,status,difficulty,problem_types,
            employment_types,topics,target_roles,assessment_platform,
            practice_format,last_seen,last_seen_max,last_seen_min,seen_count,
            order_idx,index_hash,index_json,first_indexed_at,updated_at)
        VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
        ON CONFLICT(id) DO UPDATE SET
            title=excluded.title, company=excluded.company,
            company_id=excluded.company_id, status=excluded.status,
            difficulty=excluded.difficulty, problem_types=excluded.problem_types,
            employment_types=excluded.employment_types, topics=excluded.topics,
            target_roles=excluded.target_roles,
            assessment_platform=excluded.assessment_platform,
            practice_format=excluded.practice_format,
            last_seen=excluded.last_seen, last_seen_max=excluded.last_seen_max,
            last_seen_min=excluded.last_seen_min, seen_count=excluded.seen_count,
            order_idx=excluded.order_idx, index_hash=excluded.index_hash,
            index_json=excluded.index_json, updated_at=excluded.updated_at,
            -- index row changed, so the cached detail is stale
            detail_json=NULL, detail_fetched_at=NULL
    """, rows)
    conn.commit()
    return new, changed


# --------------------------------------------------------------------------
# sync
# --------------------------------------------------------------------------
def cmd_sync(args) -> int:
    conn = connect(args.db)
    throttle = Throttle(rps=args.rps, burst=args.burst)
    client = Client(throttle, args.workers, args.user_agent,
                    args.cookie or os.environ.get("FASTPREP_COOKIE"),
                    args.timeout, args.max_retries)
    started = now_iso()

    log(f"fetching index: {INDEX_URL}")
    index = client.get_json(INDEX_URL)
    if not isinstance(index, list):
        log("unexpected index payload")
        return 1
    log(f"index: {len(index)} problems")
    new, changed = upsert_index(conn, index)
    log(f"index stored: {new} new, {changed} changed, "
        f"{len(index) - new - changed} unchanged")

    if args.index_only:
        conn.execute("INSERT INTO sync_runs VALUES (?,?,?,?,?,?)",
                     (started, now_iso(), len(index), 0, 0, "index-only"))
        conn.commit()
        log("done (index only)")
        return 0

    # which details still need fetching
    where = "detail_json IS NULL"
    params: list = []
    if args.refresh:
        where = "1=1"
    if args.stage:
        where += " AND problem_types LIKE ?"
        params.append(f'%"{resolve_stage(args.stage)}"%')
    if args.company:
        where += " AND company = ?"
        params.append(args.company)
    order = "last_seen_max DESC NULLS LAST" if args.recent_first else "id"
    sql = f"SELECT id FROM problems WHERE {where} ORDER BY {order}"
    if args.limit:
        sql += f" LIMIT {int(args.limit)}"
    todo = [r["id"] for r in conn.execute(sql, params)]

    if not todo:
        log("no details to fetch - everything is up to date")
        return 0

    eta = len(todo) / max(throttle.rps, 0.01)
    log(f"fetching {len(todo)} details with {args.workers} workers at "
        f"~{args.rps} req/s (eta ~{eta/60:.1f} min)")

    write_lock = threading.Lock()
    done = errors = 0
    stop = threading.Event()

    def work(pid: str):
        if stop.is_set():
            return pid, None, "stopped"
        try:
            d = client.get_json(DETAIL_URL.format(id=pid))
            return pid, d, None
        except Exception as e:  # noqa: BLE001 - reported per-item, run continues
            return pid, None, str(e)

    try:
        with ThreadPoolExecutor(max_workers=args.workers) as pool:
            futures = {pool.submit(work, p): p for p in todo}
            for fut in as_completed(futures):
                pid, detail, err = fut.result()
                if err == "stopped":
                    continue
                if err:
                    errors += 1
                    log(f"  ! {pid}: {err}")
                    continue
                if detail is None:
                    errors += 1
                    log(f"  ! {pid}: 404 (delisted?)")
                    continue
                with write_lock:
                    conn.execute(
                        "UPDATE problems SET detail_json=?, detail_fetched_at=?,"
                        " updated_at=? WHERE id=?",
                        (_j(detail), now_iso(), now_iso(), pid))
                    done += 1
                    if done % 50 == 0:
                        conn.commit()
                        log(f"  {done}/{len(todo)} ({throttle.rps:.2f} req/s, "
                            f"{errors} errors)")
    except KeyboardInterrupt:
        stop.set()
        log("interrupted - committing what we have (re-run to resume)")
    finally:
        conn.commit()

    conn.execute("INSERT INTO sync_runs VALUES (?,?,?,?,?,?)",
                 (started, now_iso(), len(index), done, errors, "full"))
    conn.commit()
    log(f"done: {done} details fetched, {errors} errors -> {args.db}")
    return 0


def resolve_stage(stage: str) -> str:
    key = stage.strip().lower()
    if key in STAGE_ALIASES:
        return STAGE_ALIASES[key]
    return stage.upper()


# --------------------------------------------------------------------------
# queries
# --------------------------------------------------------------------------
def build_filter(args) -> tuple[str, list]:
    where, params = ["1=1"], []
    if getattr(args, "stage", None):
        where.append("problem_types LIKE ?")
        params.append(f'%"{resolve_stage(args.stage)}"%')
    if getattr(args, "company", None):
        where.append("company LIKE ?")
        params.append(f"%{args.company}%")
    if getattr(args, "difficulty", None):
        where.append("difficulty = ?")
        params.append(args.difficulty.lower())
    if getattr(args, "topic", None):
        where.append("topics LIKE ?")
        params.append(f'%"{args.topic.lower()}"%')
    if getattr(args, "platform", None):
        where.append("assessment_platform = ?")
        params.append(args.platform.lower())
    if getattr(args, "employment", None):
        where.append("employment_types LIKE ?")
        params.append(f'%"{args.employment.upper()}"%')
    if getattr(args, "since", None):
        where.append("last_seen_max >= ?")
        params.append(args.since)
    return " AND ".join(where), params


SORTS = {
    "recent": "last_seen_max DESC NULLS LAST, seen_count DESC, company, title",
    "oldest": "last_seen_max ASC NULLS LAST, company, title",
    "frequency": "seen_count DESC, last_seen_max DESC NULLS LAST",
    "company": "company, order_idx, title",
    "difficulty": "CASE difficulty WHEN 'easy' THEN 1 WHEN 'medium' THEN 2 "
                  "WHEN 'hard' THEN 3 ELSE 4 END, last_seen_max DESC NULLS LAST",
    "title": "title",
}


def cmd_list(args) -> int:
    conn = connect(args.db)
    where, params = build_filter(args)
    sql = (f"SELECT id,title,company,difficulty,last_seen_max,seen_count,"
           f"problem_types,topics,assessment_platform FROM problems "
           f"WHERE {where} ORDER BY {SORTS[args.sort]} LIMIT {int(args.limit)}")
    rows = list(conn.execute(sql, params))
    if args.json:
        print(json.dumps([dict(r) for r in rows], indent=2))
        return 0
    if not rows:
        print("no matches (did you run `sync` first?)")
        return 0
    print(f"{'LAST SEEN':<11} {'#':>2} {'COMPANY':<20} {'DIFF':<7} "
          f"{'STAGE':<16} TITLE")
    print("-" * 110)
    for r in rows:
        stages = ",".join(json.loads(r["problem_types"] or "[]"))
        print(f"{r['last_seen_max'] or '-':<11} {r['seen_count'] or 0:>2} "
              f"{(r['company'] or '')[:20]:<20} {(r['difficulty'] or '-'):<7} "
              f"{stages[:16]:<16} {r['title']}")
    print(f"\n{len(rows)} shown.")
    return 0


def cmd_show(args) -> int:
    conn = connect(args.db)
    row = conn.execute("SELECT * FROM problems WHERE id=?", (args.id,)).fetchone()
    if not row:
        print(f"not found: {args.id}")
        return 1
    if not row["detail_json"]:
        print("no detail cached; run: sync")
        return 1
    d = json.loads(row["detail_json"])
    if args.json:
        print(json.dumps(d, indent=2))
        return 0
    print(render_markdown(d))
    return 0


def html_to_text(s: str) -> str:
    """Good-enough HTML -> text for statements/constraints."""
    import html
    import re
    if not s:
        return ""
    s = re.sub(r"</(p|div|li|ul|ol|h\d)>", "\n", s)
    s = re.sub(r"<li>", "  - ", s)
    s = re.sub(r"<br\s*/?>", "\n", s)
    s = re.sub(r"<[^>]+>", "", s)
    s = html.unescape(s)
    return re.sub(r"\n{3,}", "\n\n", s).strip()


def render_markdown(d: dict) -> str:
    out = [f"# {d.get('title')}  ({d.get('company')})", ""]
    meta = [
        f"id: `{d.get('id')}`",
        f"difficulty: {d.get('difficulty')}",
        f"stage: {', '.join(d.get('problemTypes') or [])}",
        f"platform: {d.get('assessmentPlatform')}",
        f"topics: {', '.join(d.get('topics') or [])}",
        f"last seen: {', '.join(d.get('lastSeen') or [])}",
        f"employment: {', '.join(d.get('employmentTypes') or [])}",
    ]
    out += ["> " + " | ".join(m for m in meta if m), ""]
    out += ["## Problem", "", html_to_text(d.get("problemStatement", "")), ""]
    if d.get("constraints"):
        out += ["## Constraints", "", html_to_text(d["constraints"]), ""]
    for ex in d.get("examples") or []:
        out.append(f"### Example {ex.get('id')}")
        for i in ex.get("inputText") or []:
            out.append(f"- **{i.get('inputName')}** (`{i.get('inputType')}`) = "
                       f"`{i.get('inputValue')}`")
        out.append(f"- **output** (`{ex.get('outputType')}`) = `{ex.get('outputText')}`")
        if ex.get("explanation"):
            out += ["", html_to_text(ex["explanation"])]
        out.append("")
    if d.get("tabular"):
        out += ["## Table schemas", "", "```json",
                json.dumps(d["tabular"].get("inputSchema"), indent=2), "```", ""]
    if d.get("starterCode"):
        out += ["## Starter code", "", "```", d["starterCode"], "```", ""]
    if d.get("sourceNote"):
        out += ["## Source note", "", d["sourceNote"], ""]
    return "\n".join(out)


def cmd_export(args) -> int:
    conn = connect(args.db)
    where, params = build_filter(args)
    sql = (f"SELECT * FROM problems WHERE {where} "
           f"ORDER BY {SORTS[args.sort]} LIMIT {int(args.limit)}")
    rows = list(conn.execute(sql, params))
    out = open(args.out, "w", encoding="utf-8") if args.out else sys.stdout
    try:
        if args.format == "json":
            payload = []
            for r in rows:
                rec = json.loads(r["index_json"])
                if r["detail_json"]:
                    rec = {**rec, **json.loads(r["detail_json"])}
                payload.append(rec)
            json.dump(payload, out, indent=2, ensure_ascii=False)
        elif args.format == "jsonl":
            for r in rows:
                rec = json.loads(r["index_json"])
                if r["detail_json"]:
                    rec = {**rec, **json.loads(r["detail_json"])}
                out.write(json.dumps(rec, ensure_ascii=False) + "\n")
        elif args.format == "csv":
            import csv
            w = csv.writer(out)
            w.writerow(["id", "title", "company", "difficulty", "stages",
                        "topics", "platform", "last_seen_max", "seen_count",
                        "employment_types"])
            for r in rows:
                w.writerow([
                    r["id"], r["title"], r["company"], r["difficulty"],
                    "|".join(json.loads(r["problem_types"] or "[]")),
                    "|".join(json.loads(r["topics"] or "[]")),
                    r["assessment_platform"], r["last_seen_max"],
                    r["seen_count"],
                    "|".join(json.loads(r["employment_types"] or "[]")),
                ])
        else:  # md
            for r in rows:
                if not r["detail_json"]:
                    continue
                out.write(render_markdown(json.loads(r["detail_json"])))
                out.write("\n\n---\n\n")
    finally:
        if args.out:
            out.close()
            log(f"wrote {len(rows)} problems -> {args.out}")
    return 0


def cmd_stats(args) -> int:
    conn = connect(args.db)
    q = lambda s, p=(): list(conn.execute(s, p))  # noqa: E731
    total = q("SELECT COUNT(*) c FROM problems")[0]["c"]
    if not total:
        print("empty db - run `sync` first")
        return 0
    detailed = q("SELECT COUNT(*) c FROM problems WHERE detail_json IS NOT NULL")[0]["c"]
    print(f"problems: {total}   details cached: {detailed} "
          f"({detailed/total*100:.0f}%)\n")
    for label, sql in [
        ("stage", "SELECT problem_types k, COUNT(*) c FROM problems GROUP BY k ORDER BY c DESC LIMIT 8"),
        ("difficulty", "SELECT difficulty k, COUNT(*) c FROM problems GROUP BY k ORDER BY c DESC"),
        ("platform", "SELECT assessment_platform k, COUNT(*) c FROM problems GROUP BY k ORDER BY c DESC LIMIT 8"),
        ("top companies", "SELECT company k, COUNT(*) c FROM problems GROUP BY k ORDER BY c DESC LIMIT 10"),
    ]:
        print(f"--- {label} ---")
        for r in q(sql):
            print(f"  {str(r['k'])[:40]:<42} {r['c']}")
        print()
    print("--- newest sightings ---")
    for r in q("SELECT last_seen_max d, COUNT(*) c FROM problems "
               "WHERE d IS NOT NULL GROUP BY d ORDER BY d DESC LIMIT 10"):
        print(f"  {r['d']}  {r['c']}")
    print("\n--- recent OA problems ---")
    for r in q("SELECT title,company,last_seen_max FROM problems "
               "WHERE problem_types LIKE '%\"OA\"%' "
               "ORDER BY last_seen_max DESC NULLS LAST LIMIT 10"):
        print(f"  {r['last_seen_max']}  {r['company'][:18]:<20} {r['title']}")
    return 0



def cmd_sql(args) -> int:
    """Read-only SQL console. Blocks anything that could write."""
    conn = sqlite3.connect(f"file:{args.db}?mode=ro", uri=True)
    conn.row_factory = sqlite3.Row
    q = args.query
    if not q:
        print("enter SQL, blank line to run, Ctrl-D to quit\n"
              "  tables: problems, sync_runs   (try: .schema  /  .cols)")
        buf = []
        while True:
            try:
                line = input("sql> " if not buf else "...> ")
            except EOFError:
                print(); return 0
            if line.strip() == ".schema":
                for r in conn.execute("SELECT sql FROM sqlite_master WHERE type='table'"):
                    print(r[0])
                continue
            if line.strip() == ".cols":
                print(", ".join(c[1] for c in conn.execute("PRAGMA table_info(problems)")))
                continue
            if line.strip():
                buf.append(line); continue
            if buf:
                run_query(conn, " ".join(buf), args); buf = []
    return run_query(conn, q, args)


def run_query(conn, q, args) -> int:
    if re.search(r"\b(insert|update|delete|drop|alter|create|replace|attach|pragma)\b",
                 q, re.I):
        print("read-only console: that statement is not allowed")
        return 1
    try:
        rows = list(conn.execute(q))
    except sqlite3.Error as e:
        print(f"SQL error: {e}")
        return 1
    if not rows:
        print("(no rows)")
        return 0
    if args.json:
        print(json.dumps([dict(r) for r in rows], indent=2, ensure_ascii=False))
        return 0
    cols = rows[0].keys()
    widths = [max(len(c), max(len(str(r[c])[:40]) for r in rows)) for c in cols]
    print("  ".join(c.ljust(w) for c, w in zip(cols, widths)))
    print("  ".join("-" * w for w in widths))
    for r in rows:
        print("  ".join(str(r[c])[:40].ljust(w) for c, w in zip(cols, widths)))
    print(f"\n{len(rows)} rows")
    return 0


def cmd_schema(args) -> int:
    """Print the exact shape of detail_json - what an app consumes."""
    conn = connect(args.db)
    row = conn.execute("SELECT detail_json FROM problems WHERE detail_json IS NOT NULL "
                       "AND practice_format=? LIMIT 1", (args.format,)).fetchone()
    if not row:
        print(f"no cached {args.format} problem"); return 1
    d = json.loads(row["detail_json"])

    def walk(v, path="", depth=0):
        pad = "  " * depth
        if isinstance(v, dict):
            for k, sub in v.items():
                t = type(sub).__name__
                if isinstance(sub, (dict, list)):
                    print(f"{pad}{k:<22} {t}")
                    walk(sub, f"{path}.{k}", depth + 1)
                else:
                    prev = json.dumps(sub, ensure_ascii=False)[:60]
                    print(f"{pad}{k:<22} {t:<6} {prev}")
        elif isinstance(v, list):
            if not v:
                print(f"{pad}[] (empty)")
            else:
                print(f"{pad}[{len(v)} items], each:")
                walk(v[0], path + "[0]", depth + 1)
    print(f"# detail_json shape  (practice_format = {args.format})\n")
    walk(d)
    return 0


# --------------------------------------------------------------------------
def main() -> int:
    ap = argparse.ArgumentParser(
        description="Fetch and query the FastPrep problem bank.")
    ap.add_argument("--db", default=DEFAULT_DB)
    sub = ap.add_subparsers(dest="cmd", required=True)

    s = sub.add_parser("sync", help="fetch index + problem details")
    s.add_argument("--workers", type=int, default=5,
                   help="parallel detail fetchers (default 5)")
    s.add_argument("--rps", type=float, default=3.0,
                   help="sustained requests/sec ceiling (default 3.0)")
    s.add_argument("--burst", type=float, default=3.0)
    s.add_argument("--timeout", type=float, default=45.0)
    s.add_argument("--max-retries", type=int, default=5)
    s.add_argument("--index-only", action="store_true",
                   help="one request, metadata only")
    s.add_argument("--refresh", action="store_true",
                   help="refetch details even if cached")
    s.add_argument("--recent-first", action="store_true",
                   help="fetch newest-sighted problems first")
    s.add_argument("--stage"); s.add_argument("--company")
    s.add_argument("--limit", type=int)
    s.add_argument("--user-agent", default=DEFAULT_UA)
    s.add_argument("--cookie", help="optional; or set FASTPREP_COOKIE")
    s.set_defaults(func=cmd_sync)

    def add_filters(p):
        p.add_argument("--stage", help="oa | phone | onsite")
        p.add_argument("--company"); p.add_argument("--difficulty")
        p.add_argument("--topic"); p.add_argument("--platform")
        p.add_argument("--employment", help="INTERN | NEW GRAD | FULLTIME")
        p.add_argument("--since", help="only seen on/after YYYY-MM-DD")
        p.add_argument("--sort", choices=list(SORTS), default="recent")
        p.add_argument("--limit", type=int, default=50)

    l = sub.add_parser("list"); add_filters(l)
    l.add_argument("--json", action="store_true"); l.set_defaults(func=cmd_list)

    sh = sub.add_parser("show"); sh.add_argument("id")
    sh.add_argument("--json", action="store_true"); sh.set_defaults(func=cmd_show)

    e = sub.add_parser("export"); add_filters(e)
    e.add_argument("--format", choices=["json", "jsonl", "csv", "md"], default="json")
    e.add_argument("--out"); e.set_defaults(func=cmd_export)
    e.set_defaults(limit=100000)

    st = sub.add_parser("stats"); st.set_defaults(func=cmd_stats)

    sq = sub.add_parser("sql", help="read-only SQL console")
    sq.add_argument("query", nargs="?", help="SQL; omit for interactive mode")
    sq.add_argument("--json", action="store_true"); sq.set_defaults(func=cmd_sql)

    sc = sub.add_parser("schema", help="show detail_json structure")
    sc.add_argument("--format", choices=["algorithm", "tabular"], default="algorithm")
    sc.set_defaults(func=cmd_schema)

    args = ap.parse_args()
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
