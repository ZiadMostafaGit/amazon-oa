"""Keep the bank current while the app runs.

A background thread asks FastPrep for its index (one request), compares it with
fastprep.db, and fetches the detail of only what is new or changed - the same
`sync_bank` the scraper's own `sync` command runs, on its own write connection.
Each problem lands whole (see fastprep.sync_bank), so the app keeps serving
throughout. Afterwards everything derived from the bank is brought up to date:
the read-only Bank drops its search index so new problems are searchable, the
study space's topic map is rebuilt so they are filed under their topics, and
the JSON export next to the bank is rewritten so the two copies never disagree.

Nothing here runs under --offline, and a check never overlaps another one.
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
import threading
import time
import traceback

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, ".."))
import fastprep                                  # noqa: E402  (the scraper)

DEFAULT_INTERVAL = 6 * 3600       # the bank is updated daily; four looks a day is plenty
FIRST_CHECK_DELAY = 10            # let the server come up before touching the network


def default_export_path(db_path: str) -> str | None:
    """all_problems.json beside the bank, if the bank has one to keep in step."""
    path = os.path.join(os.path.dirname(os.path.abspath(db_path)), "all_problems.json")
    return path if os.path.exists(path) else None


def write_export(conn, path: str) -> int:
    """Rewrite the JSON export atomically: a reader sees the old file or the new."""
    rows = list(conn.execute(
        "SELECT index_json, detail_json FROM problems ORDER BY %s" % fastprep.SORTS["recent"]))
    tmp = path + ".tmp"
    with open(tmp, "w", encoding="utf-8") as out:
        fastprep.write_export(rows, "json", out)
    os.replace(tmp, path)
    return len(rows)


def write_topic_index(db_path: str, path: str) -> None:
    """Re-file every problem under the study topics (tools/topicmap.py).

    About a minute of pure CPU for the whole bank, so it runs in its own
    process: in this one it would hold the GIL and stall every request.
    """
    subprocess.run([sys.executable, os.path.join(HERE, "tools", "topicmap.py"),
                    "--db", db_path, "--out", path, "--quiet"],
                   check=True, timeout=900, stdout=subprocess.DEVNULL)
    # topics.index() notices the new mtime and reloads


class BankSync:
    def __init__(self, db_path: str, bank=None, interval: float = DEFAULT_INTERVAL,
                 base: str = fastprep.BASE, export_path: str | None = None,
                 workers: int = 2, rps: float = 1.0, first_delay: float = FIRST_CHECK_DELAY,
                 progress=None, topic_index: str | None = None):
        self.db_path = os.path.abspath(db_path)
        self.bank = bank
        self.progress = progress
        self.interval = float(interval)
        self.base = base.rstrip("/")
        self.export_path = export_path
        self.topic_index = topic_index
        self.workers = workers
        self.rps = rps
        self.first_delay = first_delay
        self._wake = threading.Event()
        self._stop = threading.Event()
        self._lock = threading.Lock()
        self._thread: threading.Thread | None = None
        self._state = {
            "enabled": True, "running": False, "phase": "idle",
            "intervalSeconds": self.interval, "upstream": self.base,
            "lastCheck": None, "nextCheck": None, "lastResult": None,
            "lastError": None, "done": 0, "total": 0, "errors": 0,
            "exportPath": self.export_path,
        }

    # ------------------------------------------------------------ control
    def start(self) -> "BankSync":
        self._set(nextCheck=_iso(time.time() + self.first_delay))
        self._thread = threading.Thread(target=self._loop, name="banksync", daemon=True)
        self._thread.start()
        return self

    def stop(self) -> None:
        self._stop.set()
        self._wake.set()

    def trigger(self) -> bool:
        """Ask for a check now. False when one is already under way."""
        with self._lock:
            if self._state["running"]:
                return False
            self._state["phase"] = "queued"
        self._wake.set()
        return True

    def status(self) -> dict:
        with self._lock:
            return json.loads(json.dumps(self._state))

    # -------------------------------------------------------------- work
    def _set(self, **kw) -> None:
        with self._lock:
            self._state.update(kw)

    def _loop(self) -> None:
        self._wake.wait(self.first_delay)
        while not self._stop.is_set():
            self._wake.clear()
            self.run_once()
            self._set(nextCheck=_iso(time.time() + self.interval))
            self._wake.wait(self.interval)

    def run_once(self) -> dict | None:
        with self._lock:
            if self._state["running"]:
                return None
            self._state.update(running=True, phase="checking", done=0, total=0,
                               errors=0, lastError=None)
        conn = None
        try:
            conn = fastprep.connect(self.db_path)
            client = fastprep.Client(fastprep.Throttle(rps=self.rps, burst=self.rps),
                                     self.workers, fastprep.DEFAULT_UA, None,
                                     timeout=45.0, max_retries=4)
            summary = fastprep.sync_bank(conn, client, self.workers, on_event=self._on_event,
                                         stop=self._stop, base=self.base)
            changed = summary["added"] or summary["updated"] or \
                summary["delisted"] or summary["relisted"]
            if changed and self.bank is not None:
                self.bank.invalidate()
            if summary["imagesReplaced"]:
                import images
                for pid in summary["imagesReplaced"]:
                    images.forget(pid)
            if self.topic_index and changed:
                self._set(phase="filing")
                write_topic_index(self.db_path, self.topic_index)
            if self.export_path and (changed or not os.path.exists(self.export_path)):
                self._set(phase="exporting")
                write_export(conn, self.export_path)
            result = {k: (len(v) if isinstance(v, list) else v) for k, v in summary.items()}
            # the ids, not just the counts: the page links straight to what arrived
            result["addedIds"] = summary["added"][:50]
            result["progressOrphans"] = self._orphans(conn)
            self._set(lastResult=result, lastCheck=summary["finishedAt"])
            return summary
        except Exception as e:  # noqa: BLE001 - reported in the status, loop continues
            traceback.print_exc()
            self._set(lastError=str(e), lastCheck=fastprep.now_iso())
            return None
        finally:
            if conn is not None:
                conn.close()
            self._set(running=False, phase="idle")

    def _on_event(self, kind: str, **kw) -> None:
        if kind == "compared":
            self._set(phase="fetching" if kw["new"] + kw["changed"] + kw["incomplete"]
                      else "finishing",
                      total=kw["new"] + kw["changed"] + kw["incomplete"],
                      remote=kw["remote"], local=kw["local"])
        elif kind == "progress":
            self._set(done=kw["done"], errors=kw["errors"], total=kw["total"])

    def _orphans(self, conn) -> int | None:
        """Progress rows whose problem is not in the bank at all. Delisted
        problems are kept precisely so this stays 0."""
        if self.progress is None:
            return None
        ids = {r[0] for r in self.progress.conn.execute("SELECT problem_id FROM progress")}
        if not ids:
            return 0
        known = {r[0] for r in conn.execute("SELECT id FROM problems")}
        return len(ids - known)


class DisabledSync:
    """What the app talks to under --offline or --no-sync."""

    def __init__(self, reason: str):
        self.reason = reason

    def start(self):
        return self

    def stop(self) -> None:
        pass

    def trigger(self) -> bool:
        return False

    def status(self) -> dict:
        return {"enabled": False, "running": False, "phase": "disabled",
                "reason": self.reason}


def _iso(ts: float) -> str:
    from datetime import datetime, timezone
    return datetime.fromtimestamp(ts, timezone.utc).isoformat(timespec="seconds")
