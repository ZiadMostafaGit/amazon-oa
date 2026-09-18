"""Your own data: status, bookmarks, notes and the last code you ran.

Deliberately a separate database file. `python3 fastprep.py sync` rewrites rows
in fastprep.db, so anything of yours stored there would eventually be lost; and
that file is opened read-only everywhere else in this app.
"""

from __future__ import annotations

import json
import os
import sqlite3
import time

HERE = os.path.dirname(os.path.abspath(__file__))
DEFAULT_PATH = os.path.join(HERE, "progress.db")

SCHEMA = """
CREATE TABLE IF NOT EXISTS progress (
    problem_id  TEXT PRIMARY KEY,
    status      TEXT,              -- attempted | solved | review | NULL
    bookmarked  INTEGER DEFAULT 0,
    notes       TEXT,
    updated_at  TEXT
);
CREATE TABLE IF NOT EXISTS submissions (
    problem_id  TEXT,
    language    TEXT,
    code        TEXT,
    passed      INTEGER,
    total       INTEGER,
    ran_at      TEXT,
    PRIMARY KEY (problem_id, language)
);
CREATE TABLE IF NOT EXISTS run_log (
    problem_id TEXT, language TEXT, passed INTEGER, total INTEGER, ran_at TEXT
);
CREATE TABLE IF NOT EXISTS custom_cases (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    problem_id  TEXT NOT NULL,
    inputs      TEXT,              -- json: [{name, type, rawValue}]
    expected    TEXT,              -- the expected output, as the bank writes it
    note        TEXT,
    created_at  TEXT
);
CREATE TABLE IF NOT EXISTS topic_progress (
    slug        TEXT PRIMARY KEY,
    status      TEXT,              -- reading | done | NULL
    notes       TEXT,
    checked     TEXT,              -- json: ids of revealed self-check questions
    scratch     TEXT,              -- code typed into the article's snippets
    updated_at  TEXT
);
CREATE INDEX IF NOT EXISTS idx_status ON progress(status);
CREATE INDEX IF NOT EXISTS idx_cases  ON custom_cases(problem_id);
"""

STATUSES = ("attempted", "solved", "review")


class Progress:
    def __init__(self, path: str = DEFAULT_PATH):
        self.path = path
        self.conn = sqlite3.connect(path, check_same_thread=False)
        self.conn.row_factory = sqlite3.Row
        self.conn.execute("PRAGMA journal_mode=WAL")
        self.conn.executescript(SCHEMA)
        self.conn.commit()

    @staticmethod
    def _now() -> str:
        return time.strftime("%Y-%m-%dT%H:%M:%S")

    # ------------------------------------------------------------------ read
    def get(self, pid: str) -> dict:
        r = self.conn.execute("SELECT * FROM progress WHERE problem_id=?", (pid,)).fetchone()
        out = {"problemId": pid, "status": None, "bookmarked": False, "notes": "",
               "updatedAt": None, "submissions": {}}
        if r:
            out.update(status=r["status"], bookmarked=bool(r["bookmarked"]),
                       notes=r["notes"] or "", updatedAt=r["updated_at"])
        for s in self.conn.execute("SELECT * FROM submissions WHERE problem_id=?", (pid,)):
            out["submissions"][s["language"]] = {
                "code": s["code"], "passed": s["passed"], "total": s["total"],
                "ranAt": s["ran_at"]}
        return out

    def all(self) -> dict:
        out = {}
        for r in self.conn.execute("SELECT * FROM progress"):
            if r["status"] or r["bookmarked"] or (r["notes"] or "").strip():
                out[r["problem_id"]] = {"status": r["status"],
                                        "bookmarked": bool(r["bookmarked"]),
                                        "hasNotes": bool((r["notes"] or "").strip())}
        return out

    def ids_with(self, status: str | None = None, bookmarked: bool = False,
                 has_notes: bool = False) -> list[str]:
        sql, args = ["SELECT problem_id FROM progress WHERE 1=1"], []
        if status == "none":
            return []                      # handled by the caller (set difference)
        if status:
            sql.append("AND status=?"); args.append(status)
        if bookmarked:
            sql.append("AND bookmarked=1")
        if has_notes:
            sql.append("AND TRIM(COALESCE(notes,'')) <> ''")
        return [r[0] for r in self.conn.execute(" ".join(sql), args)]

    # -------------------------------------------------------- study space
    def topic_get(self, slug: str) -> dict:
        r = self.conn.execute("SELECT * FROM topic_progress WHERE slug=?",
                              (slug,)).fetchone()
        if not r:
            return {"slug": slug, "status": None, "notes": "", "checked": [],
                    "scratch": {}, "updatedAt": None}
        return {"slug": slug, "status": r["status"], "notes": r["notes"] or "",
                "checked": json.loads(r["checked"] or "[]"),
                "scratch": json.loads(r["scratch"] or "{}"),
                "updatedAt": r["updated_at"]}

    def topics_all(self) -> dict:
        out = {}
        for r in self.conn.execute("SELECT * FROM topic_progress"):
            if r["status"] or (r["notes"] or "").strip():
                out[r["slug"]] = {"status": r["status"],
                                  "hasNotes": bool((r["notes"] or "").strip())}
        return out

    def topic_update(self, slug: str, **fields) -> dict:
        cur = self.topic_get(slug)
        sets, args = [], []
        for key, col in (("status", "status"), ("notes", "notes")):
            if key in fields:
                v = fields[key]
                if key == "status" and v not in (None, "", "reading", "done"):
                    raise ValueError("unknown study status: %r" % (v,))
                sets.append("%s=?" % col); args.append(v or None if key == "status" else (v or ""))
        for key, col in (("checked", "checked"), ("scratch", "scratch")):
            if key in fields:
                sets.append("%s=?" % col); args.append(json.dumps(fields[key]))
        if not sets:
            return cur
        self.conn.execute(
            "INSERT INTO topic_progress(slug, updated_at) VALUES (?,?) "
            "ON CONFLICT(slug) DO NOTHING", (slug, self._now()))
        self.conn.execute("UPDATE topic_progress SET %s, updated_at=? WHERE slug=?"
                          % ", ".join(sets), args + [self._now(), slug])
        self.conn.commit()
        return self.topic_get(slug)

    def stats(self) -> dict:
        rows = dict(self.conn.execute(
            "SELECT COALESCE(status,'none'), COUNT(*) FROM progress GROUP BY 1").fetchall())
        rows["bookmarked"] = self.conn.execute(
            "SELECT COUNT(*) FROM progress WHERE bookmarked=1").fetchone()[0]
        rows["runs"] = self.conn.execute("SELECT COUNT(*) FROM run_log").fetchone()[0]
        rows["topicsRead"] = self.conn.execute(
            "SELECT COUNT(*) FROM topic_progress WHERE status='done'").fetchone()[0]
        return rows

    # ----------------------------------------------------------------- write
    def update(self, pid: str, **fields) -> dict:
        cur = self.get(pid)
        status = fields.get("status", cur["status"])
        if status in ("", "none"):
            status = None
        if status is not None and status not in STATUSES:
            raise ValueError("unknown status %r" % (status,))
        bookmarked = fields.get("bookmarked", cur["bookmarked"])
        notes = fields.get("notes", cur["notes"])
        self.conn.execute(
            "INSERT INTO progress(problem_id, status, bookmarked, notes, updated_at) "
            "VALUES (?,?,?,?,?) ON CONFLICT(problem_id) DO UPDATE SET "
            "status=excluded.status, bookmarked=excluded.bookmarked, "
            "notes=excluded.notes, updated_at=excluded.updated_at",
            (pid, status, 1 if bookmarked else 0, notes, self._now()))
        self.conn.commit()
        return self.get(pid)

    def save_submission(self, pid: str, language: str, code: str,
                        passed: int | None = None, total: int | None = None) -> None:
        now = self._now()
        self.conn.execute(
            "INSERT INTO submissions(problem_id, language, code, passed, total, ran_at) "
            "VALUES (?,?,?,?,?,?) ON CONFLICT(problem_id, language) DO UPDATE SET "
            "code=excluded.code, passed=excluded.passed, total=excluded.total, "
            "ran_at=excluded.ran_at", (pid, language, code, passed, total, now))
        if passed is not None:
            self.conn.execute(
                "INSERT INTO run_log(problem_id, language, passed, total, ran_at) "
                "VALUES (?,?,?,?,?)", (pid, language, passed, total, now))
            # a clean sweep of the visible examples counts as attempted, never
            # as solved: there are no hidden tests in this data to prove more
            row = self.conn.execute("SELECT status FROM progress WHERE problem_id=?",
                                    (pid,)).fetchone()
            if not row or not row["status"]:
                self.conn.execute(
                    "INSERT INTO progress(problem_id, status, bookmarked, notes, updated_at) "
                    "VALUES (?,?,0,'',?) ON CONFLICT(problem_id) DO UPDATE SET "
                    "status=COALESCE(progress.status, excluded.status), "
                    "updated_at=excluded.updated_at", (pid, "attempted", now))
        self.conn.commit()

    # ----------------------------------------------------------- custom cases
    def cases(self, pid: str) -> list:
        out = []
        for r in self.conn.execute(
                "SELECT * FROM custom_cases WHERE problem_id=? ORDER BY id", (pid,)):
            out.append({"caseId": r["id"], "inputs": json.loads(r["inputs"] or "[]"),
                        "expectedRaw": r["expected"], "note": r["note"] or "",
                        "createdAt": r["created_at"], "custom": True})
        return out

    def add_case(self, pid: str, inputs: list, expected: str, note: str = "") -> dict:
        cur = self.conn.execute(
            "INSERT INTO custom_cases(problem_id, inputs, expected, note, created_at) "
            "VALUES (?,?,?,?,?)",
            (pid, json.dumps(inputs), expected, note, self._now()))
        self.conn.commit()
        return {"caseId": cur.lastrowid}

    def update_case(self, case_id: int, inputs=None, expected=None, note=None) -> None:
        row = self.conn.execute("SELECT * FROM custom_cases WHERE id=?", (case_id,)).fetchone()
        if not row:
            raise ValueError("no custom case %r" % case_id)
        self.conn.execute(
            "UPDATE custom_cases SET inputs=?, expected=?, note=? WHERE id=?",
            (json.dumps(inputs) if inputs is not None else row["inputs"],
             row["expected"] if expected is None else expected,
             row["note"] if note is None else note, case_id))
        self.conn.commit()

    def delete_case(self, case_id: int) -> None:
        self.conn.execute("DELETE FROM custom_cases WHERE id=?", (case_id,))
        self.conn.commit()

    def export(self) -> dict:
        return {
            "version": 1,
            "exportedAt": self._now(),
            "progress": [dict(r) for r in self.conn.execute("SELECT * FROM progress")],
            "submissions": [dict(r) for r in self.conn.execute("SELECT * FROM submissions")],
            "customCases": [dict(r) for r in self.conn.execute("SELECT * FROM custom_cases")],
            "topics": [dict(r) for r in self.conn.execute("SELECT * FROM topic_progress")],
        }
