"""The reference-solution store.

One file per problem under solutions/, named by problem id: `<id>.py` for an
algorithm problem, `<id>.sql` for a tabular one. The bank ships no solutions
and no hidden tests, so a solution is only ever offered after it has been run
against that problem's visible examples - `tools/verify.py --all` records the
outcome in solutions/VERIFIED.json, and anything not in there is presented as
unverified.
"""

from __future__ import annotations

import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
DIR = os.path.join(HERE, "solutions")
INDEX = os.path.join(DIR, "VERIFIED.json")
MANIFEST = os.path.join(DIR, "MANIFEST.json")


def path_for(pid: str, fmt: str = "algorithm") -> str:
    return os.path.join(DIR, "%s%s" % (pid, ".sql" if fmt == "tabular" else ".py"))


def _index() -> dict:
    try:
        with open(INDEX, "r", encoding="utf-8") as f:
            return json.load(f).get("problems", {})
    except (FileNotFoundError, json.JSONDecodeError):
        return {}


def get(pid: str, fmt: str = "algorithm") -> dict | None:
    """The stored solution for a problem, with its verification state."""
    path = path_for(pid, fmt)
    if not os.path.exists(path):
        return None
    with open(path, "r", encoding="utf-8") as f:
        code = f.read()
    entry = _index().get(pid) or {}
    return {
        "code": code,
        "language": "sql" if path.endswith(".sql") else "python",
        "verified": bool(entry.get("ok")),
        "cases": entry.get("cases"),
        "checkedAt": entry.get("checkedAt"),
        "note": entry.get("note"),
    }


def stats() -> dict:
    idx = _index()
    have = sum(1 for n in os.listdir(DIR) if n.endswith((".py", ".sql"))) if os.path.isdir(DIR) else 0
    try:
        with open(MANIFEST, "r", encoding="utf-8") as f:
            targeted = json.load(f).get("count", 0)
    except (FileNotFoundError, json.JSONDecodeError):
        targeted = 0
    return {"stored": have, "verified": sum(1 for v in idx.values() if v.get("ok")),
            "targeted": targeted}
