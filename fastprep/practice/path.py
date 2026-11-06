"""The DSA learning path, served: path/PATH.json joined with the bank and your progress.

PATH.json is built by tools/path.py (topics in learning order, problems in solving order,
each stage tied to a KHATT week). This module only reads it: the listing for the Path view,
and where one problem sits in it, so a problem can offer "next in path".
"""

from __future__ import annotations

import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
PATH_JSON = os.path.join(HERE, "path", "PATH.json")

_cache: dict = {"mtime": None, "data": None, "where": {}}


def _load() -> dict | None:
    try:
        m = os.path.getmtime(PATH_JSON)
    except OSError:
        return None
    if _cache["mtime"] != m:
        with open(PATH_JSON, encoding="utf-8") as f:
            data = json.load(f)
        where = {}
        n = 0
        for ph in data.get("phases", []):
            for st in ph.get("stages", []):
                n += 1
                seq = st.get("plan", []) + st.get("more", [])
                for i, pid in enumerate(seq):
                    where.setdefault(pid, {"stage": st["slug"], "title": st["title"], "number": n,
                                           "week": st.get("week"), "index": i, "seq": seq,
                                           "inPlan": i < len(st.get("plan", [])), "planSize": len(st.get("plan", []))})
        _cache.update(mtime=m, data=data, where=where)
    return _cache["data"]


def _summary(bank, pid: str, marks: dict, fixes_mod, verified: set) -> dict | None:
    d = bank.detail(pid)
    if not d:
        return None
    pr = marks.get(pid) or {}
    return {
        "id": pid, "title": d.get("title") or pid, "difficulty": (d.get("difficulty") or "").lower(),
        "company": d.get("company"), "oa": "OA" in (d.get("problemTypes") or []),
        "status": pr.get("status"), "repaired": fixes_mod.get(pid) is not None, "verified": pid in verified,
    }


def listing(bank, progress, fixes_mod, solutions_mod) -> dict:
    data = _load()
    if not data:
        return {"phases": [], "sets": [], "missing": True}
    marks = progress.all()
    try:
        verified = set(solutions_mod.verified_ids())
    except AttributeError:
        verified = set()
    out_phases, nxt, n = [], None, 0
    total = done = 0
    for ph in data["phases"]:
        stages = []
        for st in ph["stages"]:
            n += 1
            plan = [s for s in (_summary(bank, p, marks, fixes_mod, verified) for p in st["plan"]) if s]
            more = [s for s in (_summary(bank, p, marks, fixes_mod, verified) for p in st["more"]) if s]
            solved = sum(1 for s in plan if s["status"] == "solved")
            total += len(plan); done += solved
            if nxt is None:
                for s in plan:
                    if s["status"] != "solved":
                        nxt = {"id": s["id"], "title": s["title"], "stage": st["slug"], "stageTitle": st["title"], "number": n}
                        break
            stages.append(dict(st, number=n, plan=plan, more=more, solved=solved,
                               moreSolved=sum(1 for s in more if s["status"] == "solved")))
        out_phases.append(dict(ph, stages=stages))
    sets = []
    for s in data.get("sets", []):
        probs = [x for x in (_summary(bank, p, marks, fixes_mod, verified) for p in s["ids"]) if x]
        sets.append(dict(week=s["week"], label=s["label"], problems=probs,
                         solved=sum(1 for x in probs if x["status"] == "solved")))
    return {"phases": out_phases, "sets": sets, "next": nxt, "planTotal": total, "planSolved": done,
            "oaSample": data.get("oaSample"), "amazonSample": data.get("amazonSample")}


def position(pid: str, bank=None) -> dict | None:
    """Where a problem sits in the path, with its neighbours, or None."""
    _load()
    w = _cache["where"].get(pid)
    if not w:
        return None
    seq, i = w["seq"], w["index"]

    def peek(j):
        if 0 <= j < len(seq):
            t = None
            if bank is not None:
                d = bank.detail(seq[j])
                t = d.get("title") if d else None
            return {"id": seq[j], "title": t or seq[j]}
        return None
    return {"stage": w["stage"], "title": w["title"], "number": w["number"], "week": w["week"],
            "index": i, "inPlan": w["inPlan"], "planSize": w["planSize"], "total": len(seq),
            "prev": peek(i - 1), "next": peek(i + 1)}
