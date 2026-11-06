"""Hand-written repairs laid over the bank, one JSON file per problem.

The bank is FastPrep's text, and a lot of it is thin: a two-line paraphrase of
a screenshot, constraints that say "be efficient", one example. The bank is
also rewritten by every sync, so nothing can be fixed in place. A repair lives
here instead, beside the problem it repairs, and the app lays it over the
original - which always stays one click away.

    fixes/<problem-id>.json
    {
      "statement":   "<p>...</p>",   optional: a clearer statement, with a worked example
      "constraints": "<ul>...</ul>", optional: real bounds, when the source has none
      "pattern":     "knapsack",     the study-space chapter this problem is an instance of
      "why":         "...",          how the story reduces to that pattern, in a sentence or two
      "hints":       ["...", "...", "..."],   a ladder: nudge, the idea, the plan
      "pitfalls":    ["..."],        optional: the edge cases that sink a first attempt
      "by": "claude", "at": "2026-11-06"
    }

    fixes/khatt.json     {problem-id: {"week": 20, "day": "Sun", "label": "..."}}
                         - the problems the KHATT year plan schedules, so a problem
                         can say where it sits in the plan.

`python3 tools/fix.py` lists what still needs repairing and checks a repair.
"""

from __future__ import annotations

import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
DIR = os.path.join(HERE, "fixes")
KHATT = os.path.join(DIR, "khatt.json")

FIELDS = {"statement", "constraints", "pattern", "why", "hints", "pitfalls", "by", "at"}

_cache: dict = {}


def _load(path: str):
    """Read a JSON file, re-reading only when it changes on disk."""
    try:
        mtime = os.stat(path).st_mtime
    except OSError:
        _cache.pop(path, None)
        return None
    hit = _cache.get(path)
    if hit and hit[0] == mtime:
        return hit[1]
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except (OSError, json.JSONDecodeError):
        data = None
    _cache[path] = (mtime, data)
    return data


def path_for(pid: str) -> str:
    return os.path.join(DIR, pid + ".json")


def get(pid: str) -> dict | None:
    if not pid or "/" in pid or pid.startswith("."):
        return None
    data = _load(path_for(pid))
    if not isinstance(data, dict):
        return None
    return {k: v for k, v in data.items() if k in FIELDS}


def khatt_for(pid: str) -> dict | None:
    data = _load(KHATT) or {}
    return data.get(pid)


def khatt_ids() -> list:
    return list((_load(KHATT) or {}).keys())


def problems(fix: dict | None, known_patterns: set | None = None) -> list:
    """What is wrong with a repair file, as readable lines (empty when it is fine)."""
    if fix is None:
        return ["no repair file"]
    out = []
    extra = set(fix) - FIELDS
    if extra:
        out.append("unknown fields: " + ", ".join(sorted(extra)))
    hints = fix.get("hints")
    if not isinstance(hints, list) or not (2 <= len(hints) <= 4) or not all(isinstance(h, str) and h.strip() for h in hints):
        out.append("hints must be a list of 2-4 non-empty strings")
    if not isinstance(fix.get("why"), str) or len(fix.get("why", "").strip()) < 20:
        out.append("why must say how the story reduces to the pattern")
    pat = fix.get("pattern")
    if not isinstance(pat, str) or not pat:
        out.append("pattern (a study chapter slug) is missing")
    elif known_patterns is not None and pat not in known_patterns:
        out.append("pattern %r is not a study chapter" % pat)
    for k in ("statement", "constraints"):
        v = fix.get(k)
        if v is not None and (not isinstance(v, str) or "<" not in v):
            out.append(k + " must be HTML")
    if fix.get("pitfalls") is not None and not isinstance(fix.get("pitfalls"), list):
        out.append("pitfalls must be a list")
    return out
