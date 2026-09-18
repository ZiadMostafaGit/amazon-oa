"""Read-only access to the FastPrep problem bank, plus the query builder.

The bank is opened `mode=ro` everywhere: `python3 fastprep.py sync` owns that
file and a write from here would be lost (or worse, would corrupt a sync).
Progress lives in its own database - see progress.py.

Two traps this module exists to avoid:
  * stage lives in `problem_types`, a JSON array stored as TEXT. Filtering on
    the singular `problemType` inside detail_json drops 1082 of 3533 rows,
    because it is null for every problem with more than one stage. Every array
    facet here is queried with json_each().
  * `problemStatement`, `constraints` and `explanation` are HTML.
"""

from __future__ import annotations

import json
import os
import re
import sqlite3
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DEFAULT_DB = os.path.abspath(os.path.join(HERE, "..", "fastprep.db"))

sys.path.insert(0, os.path.join(HERE, ".."))
try:
    from fastprep import html_to_text          # reuse the scraper's own helper
except Exception:                              # pragma: no cover - fallback copy
    def html_to_text(s: str) -> str:
        import html as _html
        if not s:
            return ""
        s = re.sub(r"</(p|div|li|ul|ol|h\d)>", "\n", s)
        s = re.sub(r"<li>", "  - ", s)
        s = re.sub(r"<br\s*/?>", "\n", s)
        s = re.sub(r"<[^>]+>", "", s)
        return re.sub(r"\n{3,}", "\n\n", _html.unescape(s)).strip()

# Facets backed by a JSON array column, and the scalar ones.
ARRAY_FACETS = {
    "stage": "problem_types",
    "topic": "topics",
    "employment": "employment_types",
    "role": "target_roles",
}
UNSET = "__unset__"       # the facet value meaning "this field is empty"

SCALAR_FACETS = {
    "company": "company",
    "difficulty": "difficulty",
    "platform": "assessment_platform",
    "format": "practice_format",
}
# Every sortable field, with the direction supplied separately: any field can
# be read in either order, which "hardest first" and "oldest sighting" used to
# fake with a second entry per field.
# (expression, natural direction, label, "unknown" test)
# The last element keeps rows with no value at the bottom whichever way the
# sort runs: "hardest first" should start at hard, not at the 76 problems whose
# difficulty was never recorded.
SORT_FIELDS = {
    "recent":     ("p.last_seen_max", "desc", "date last seen",
                   "p.last_seen_max IS NULL"),
    "frequent":   ("COALESCE(p.seen_count, 0)", "desc", "times seen", None),
    "difficulty": ("CASE p.difficulty WHEN 'easy' THEN 0 WHEN 'medium' THEN 1 "
                   "WHEN 'hard' THEN 2 ELSE 3 END", "asc", "difficulty",
                   "p.difficulty IS NULL"),
    "title":      ("p.title COLLATE NOCASE", "asc", "title", None),
    "company":    ("p.company COLLATE NOCASE", "asc", "company", None),
    "default":    ("p.order_idx", "asc", "bank order", None),
}
# older links keep working
LEGACY_SORTS = {"oldest": ("recent", "asc"), "rare": ("frequent", "asc"),
                "hardest": ("difficulty", "desc")}
TIEBREAK = "p.title COLLATE NOCASE ASC"


def resolve_sort(sort: str, direction: str | None = None) -> tuple[str, str]:
    """(key, 'asc'|'desc'), accepting the legacy one-way sort names."""
    key = (sort or "recent").strip()
    if key in LEGACY_SORTS:
        key, implied = LEGACY_SORTS[key]
        direction = direction or implied
    if key not in SORT_FIELDS and key != "relevance":
        key = "recent"
    d = (direction or "").lower()
    if d not in ("asc", "desc"):
        d = SORT_FIELDS.get(key, ("", "desc"))[1]
    return key, d


def order_by(sort: str, direction: str | None = None) -> str:
    key, d = resolve_sort(sort, direction)
    field = SORT_FIELDS.get(key, SORT_FIELDS["recent"])
    expr, unknown = field[0], field[3]
    head = ("%s ASC, " % unknown) if unknown else ""        # unknowns last, always
    if expr == SORT_FIELDS["title"][0]:        # the tiebreak IS the key here
        return "%s%s %s" % (head, expr, d.upper())
    return "%s%s %s, %s" % (head, expr, d.upper(), TIEBREAK)
LIST_COLUMNS = """p.id, p.title, p.company, p.difficulty, p.problem_types, p.topics,
                  p.employment_types, p.target_roles, p.assessment_platform,
                  p.practice_format, p.last_seen, p.last_seen_max, p.seen_count"""


class Bank:
    def __init__(self, path: str = DEFAULT_DB):
        self.path = os.path.abspath(path)
        if not os.path.exists(self.path):
            raise FileNotFoundError(self.path)
        self.conn = sqlite3.connect("file:%s?mode=ro" % self.path, uri=True,
                                    check_same_thread=False)
        self.conn.row_factory = sqlite3.Row
        self.conn.execute("PRAGMA query_only=ON")
        self._search = None

    # ---------------------------------------------------------------- search
    def _ensure_search_index(self):
        """An FTS5 index over title + statement, built in memory at first use.

        It cannot live in the bank itself (read-only, and a sync would drop it),
        and rebuilding takes about a second for 3533 problems.
        """
        if self._search is not None:
            return
        idx = sqlite3.connect(":memory:", check_same_thread=False)
        idx.execute("CREATE VIRTUAL TABLE docs USING fts5(id UNINDEXED, title, body)")
        rows = []
        for r in self.conn.execute("SELECT id, title, detail_json FROM problems"):
            d = json.loads(r["detail_json"] or "{}")
            body = " ".join(filter(None, [
                html_to_text(d.get("problemStatement") or ""),
                html_to_text(d.get("constraints") or ""),
                d.get("sourceNote") or "",
                d.get("functionName") or "",
            ]))
            rows.append((r["id"], r["title"] or "", body))
        idx.executemany("INSERT INTO docs(id, title, body) VALUES (?,?,?)", rows)
        idx.commit()
        self._search = idx

    def _search_ids(self, query: str) -> list[str]:
        """Ranked ids for a free-text query; title matches weigh more."""
        self._ensure_search_index()
        terms = [t for t in re.split(r"[^\w]+", query or "") if t]
        if not terms:
            return []
        match = " AND ".join('"%s"*' % t.replace('"', '') for t in terms)
        try:
            cur = self._search.execute(
                "SELECT id FROM docs WHERE docs MATCH ? ORDER BY bm25(docs, 10.0, 1.0)", (match,))
            return [r[0] for r in cur]
        except sqlite3.OperationalError:
            like = "%" + query.strip() + "%"
            cur = self._search.execute(
                "SELECT id FROM docs WHERE title LIKE ? OR body LIKE ?", (like, like))
            return [r[0] for r in cur]

    # ----------------------------------------------------------------- query
    def _where(self, f: dict) -> tuple[str, list]:
        sql, args = [], []
        for key, col in SCALAR_FACETS.items():
            vals = [v for v in (f.get(key) or []) if v]
            if not vals:
                continue
            # UNSET is a real answer: 1557 problems name no platform, 76 no
            # difficulty. Without it those rows can be excluded but never found.
            named = [v for v in vals if v != UNSET]
            parts = []
            if named:
                parts.append("p.%s IN (%s)" % (col, ",".join("?" * len(named))))
                args += named
            if UNSET in vals:
                parts.append("p.%s IS NULL" % col)
            sql.append("(" + " OR ".join(parts) + ")")
        for key, col in ARRAY_FACETS.items():
            vals = [v for v in (f.get(key) or []) if v]
            if not vals:
                continue
            named = [v for v in vals if v != UNSET]
            parts = []
            if named:
                # array column -> json_each, never the singular scalar
                parts.append("EXISTS (SELECT 1 FROM json_each(p.%s) WHERE value IN (%s))"
                             % (col, ",".join("?" * len(named))))
                args += named
            if UNSET in vals:
                parts.append("json_array_length(COALESCE(p.%s, '[]')) = 0" % col)
            sql.append("(" + " OR ".join(parts) + ")")
        if f.get("seenFrom"):
            sql.append("p.last_seen_max >= ?"); args.append(f["seenFrom"])
        if f.get("seenTo"):
            sql.append("p.last_seen_max <= ?"); args.append(f["seenTo"])
        if f.get("seenOnFrom") or f.get("seenOnTo"):
            # any sighting inside the window, not just the newest one
            clause = ["EXISTS (SELECT 1 FROM json_each(p.last_seen) WHERE 1=1"]
            if f.get("seenOnFrom"):
                clause.append("AND value >= ?"); args.append(f["seenOnFrom"])
            if f.get("seenOnTo"):
                clause.append("AND value <= ?"); args.append(f["seenOnTo"])
            sql.append(" ".join(clause) + ")")
        if f.get("minSeen"):
            sql.append("COALESCE(p.seen_count, 0) >= ?"); args.append(int(f["minSeen"]))
        if f.get("maxSeen"):
            sql.append("COALESCE(p.seen_count, 0) <= ?"); args.append(int(f["maxSeen"]))
        if f.get("hasImages"):
            sql.append("json_array_length(json_extract(p.detail_json, '$.sourceImages')) > 0")
        if f.get("ids") is not None:
            ids = list(f["ids"])
            if not ids:
                return "0", []
            sql.append("p.id IN (%s)" % ",".join("?" * len(ids)))
            args += ids
        return (" AND ".join(sql) if sql else "1"), args

    def query(self, f: dict, sort: str = "recent", limit: int = 50, offset: int = 0,
              direction: str | None = None):
        """Returns {total, items, ...}. `f['q']` is full-text; `f['ids']` scopes."""
        f = dict(f or {})
        ranked = None
        if (f.get("q") or "").strip():
            ranked = self._search_ids(f["q"])
            scope = f.get("ids")
            if scope is not None:
                keep = set(scope)
                ranked = [i for i in ranked if i in keep]
            f["ids"] = ranked

        where, args = self._where(f)
        total = self.conn.execute("SELECT COUNT(*) FROM problems p WHERE " + where, args).fetchone()[0]

        if ranked is not None and sort == "relevance":
            order_ids = ranked[offset:offset + limit]
            if not order_ids:
                items = []
            else:
                rows = {r["id"]: r for r in self.conn.execute(
                    "SELECT %s FROM problems p WHERE p.id IN (%s)"
                    % (LIST_COLUMNS, ",".join("?" * len(order_ids))), order_ids)}
                items = [self._row(rows[i]) for i in order_ids if i in rows]
        else:
            order = order_by(sort, direction)
            cur = self.conn.execute(
                "SELECT %s FROM problems p WHERE %s ORDER BY %s LIMIT ? OFFSET ?"
                % (LIST_COLUMNS, where, order), args + [int(limit), int(offset)])
            items = [self._row(r) for r in cur]
        key, d = resolve_sort(sort, direction)
        return {"total": total, "items": items, "limit": limit, "offset": offset,
                "sort": sort if sort == "relevance" else key, "direction": d}

    @staticmethod
    def _row(r: sqlite3.Row) -> dict:
        j = lambda s: json.loads(s) if s else []
        return {
            "id": r["id"], "title": r["title"], "company": r["company"],
            "difficulty": r["difficulty"], "stages": j(r["problem_types"]),
            "topics": j(r["topics"]), "employmentTypes": j(r["employment_types"]),
            "targetRoles": j(r["target_roles"]), "platform": r["assessment_platform"],
            "format": r["practice_format"], "lastSeen": j(r["last_seen"]),
            "lastSeenMax": r["last_seen_max"], "seenCount": r["seen_count"],
        }

    # ----------------------------------------------------------------- facets
    def facets(self) -> dict:
        out = {}
        for key, col in SCALAR_FACETS.items():
            out[key] = [{"value": r[0], "count": r[1]} for r in self.conn.execute(
                "SELECT %s, COUNT(*) n FROM problems WHERE %s IS NOT NULL "
                "GROUP BY 1 ORDER BY n DESC, 1 ASC" % (col, col))]
        for key, col in ARRAY_FACETS.items():
            out[key] = [{"value": r[0], "count": r[1]} for r in self.conn.execute(
                "SELECT value, COUNT(*) n FROM problems, json_each(%s) "
                "GROUP BY 1 ORDER BY n DESC, 1 ASC" % col)]
        row = self.conn.execute(
            "SELECT MIN(last_seen_max) lo, MAX(last_seen_max) hi, COUNT(*) n, "
            "MAX(COALESCE(seen_count,0)) maxseen FROM problems").fetchone()
        out["meta"] = {"total": row["n"], "earliest": row["lo"], "latest": row["hi"],
                       "maxSeenCount": row["maxseen"],
                       "withImages": self.conn.execute(
                           "SELECT COUNT(*) FROM problems WHERE "
                           "json_array_length(json_extract(detail_json,'$.sourceImages')) > 0"
                       ).fetchone()[0]}
        # an "(unset)" bucket wherever one exists, so nothing is unreachable
        for key, col in SCALAR_FACETS.items():
            n = self.conn.execute(
                "SELECT COUNT(*) FROM problems WHERE %s IS NULL" % col).fetchone()[0]
            if n:
                out[key].append({"value": UNSET, "count": n, "unset": True})
        for key, col in ARRAY_FACETS.items():
            n = self.conn.execute(
                "SELECT COUNT(*) FROM problems WHERE json_array_length(COALESCE(%s,'[]'))=0"
                % col).fetchone()[0]
            if n:
                out[key].append({"value": UNSET, "count": n, "unset": True})
        out["sorts"] = [{"key": k, "label": v[2], "defaultDirection": v[1]}
                        for k, v in SORT_FIELDS.items()]
        try:
            import solutions
            out["meta"]["withSolutions"] = len(solutions.verified_ids())
        except Exception:
            out["meta"]["withSolutions"] = None
        return out

    # ----------------------------------------------------------------- detail
    def detail(self, pid: str) -> dict | None:
        r = self.conn.execute(
            "SELECT id, detail_json, last_seen, seen_count, order_idx FROM problems WHERE id=?",
            (pid,)).fetchone()
        if not r:
            return None
        d = json.loads(r["detail_json"] or "{}")
        # detail_json is the truth, but seen_count/last_seen live in the columns
        d["seenCount"] = r["seen_count"]
        if not d.get("lastSeen"):
            d["lastSeen"] = json.loads(r["last_seen"] or "[]")
        d["images"] = list(d.get("sourceImages") or [])
        return d

    def neighbours(self, pid: str, f: dict, sort: str,
                   direction: str | None = None) -> dict:
        """Previous/next id under the caller's current filter and sort."""
        res = self.query(dict(f or {}), sort=sort, limit=100000, offset=0,
                         direction=direction)
        ids = [i["id"] for i in res["items"]]
        try:
            k = ids.index(pid)
        except ValueError:
            return {"prev": None, "next": None, "index": None, "of": len(ids)}
        return {"prev": ids[k - 1] if k > 0 else None,
                "next": ids[k + 1] if k + 1 < len(ids) else None,
                "index": k + 1, "of": len(ids)}

    # -------------------------------------------------------------- examples
    @staticmethod
    def runnable_cases(detail: dict) -> list:
        """The visible examples, in the shape the runner wants."""
        cases = []
        for ex in detail.get("examples") or []:
            cases.append({
                "id": ex.get("id"),
                "inputs": [{"name": i.get("inputName"), "type": i.get("inputType"),
                            "rawValue": i.get("inputValue")}
                           for i in ex.get("inputText") or []],
                "outputType": ex.get("outputType"),
                "expectedRaw": ex.get("outputText"),
                "explanation": ex.get("explanation"),
            })
        return cases
