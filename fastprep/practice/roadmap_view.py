"""The roadmap, served: roadmap/ROADMAP.json joined with the bank, the chapters and your progress.

ROADMAP.json is assembled by tools/roadmap.py from hand-curated ladders (roadmap/nodes/*.json): a tree
of topics, each listing the techniques it teaches and, for each problem, which technique it teaches and
why. This module only reads it.
"""

from __future__ import annotations

import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
PATH_JSON = os.path.join(HERE, "roadmap", "ROADMAP.json")

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
        for nd in data.get("nodes", []):
            seq = [it["id"] for it in nd.get("ladder", [])]
            for i, it in enumerate(nd.get("ladder", [])):
                where.setdefault(it["id"], {"node": nd["id"], "title": nd["title"], "order": nd["order"], "index": i,
                                            "seq": seq, "teaches": it.get("teaches"), "level": it.get("level")})
        _cache.update(mtime=m, data=data, where=where)
    return _cache["data"]


def available() -> bool:
    d = _load()
    return bool(d and any(nd.get("ladder") for nd in d.get("nodes", [])))


def listing(bank, progress, topics_mod) -> dict:
    data = _load()
    if not data:
        return {"nodes": [], "missing": True}
    marks = progress.all()
    try:
        idx = topics_mod.index()
        ctitle = {t["slug"]: t["title"] for t in idx.get("topics", [])}
    except Exception:
        ctitle = {}
    nodes, done_nodes = [], set()
    total = solved_all = 0
    for nd in data["nodes"]:
        ladder = []
        for it in nd.get("ladder", []):
            d = bank.detail(it["id"])
            if not d:
                continue
            st = (marks.get(it["id"]) or {}).get("status")
            ladder.append({"id": it["id"], "title": d.get("title") or it["id"], "difficulty": (d.get("difficulty") or "").lower(),
                           "company": d.get("company"), "oa": "OA" in (d.get("problemTypes") or []), "status": st,
                           "teaches": it.get("teaches"), "why": it.get("why"), "level": it.get("level") or "core"})
        solved = sum(1 for x in ladder if x["status"] == "solved")
        core = [x for x in ladder if x["level"] == "core"]
        core_solved = sum(1 for x in core if x["status"] == "solved")
        total += len(ladder); solved_all += solved
        chapters = [{"slug": c, "title": ctitle.get(c, c), "hasArticle": topics_mod.has_article(c)} for c in nd["chapters"]]
        out = dict(nd, ladder=ladder, chapters=chapters, solved=solved, coreTotal=len(core), coreSolved=core_solved)
        nodes.append(out)
        # a node counts as done for unlocking once most of its core is solved
        if core and core_solved >= max(1, round(0.6 * len(core))):
            done_nodes.add(nd["id"])
    nxt = None
    for nd in sorted(nodes, key=lambda n: n["order"]):
        nd["unlocked"] = all(p in done_nodes for p in nd["parents"])
        nd["done"] = nd["id"] in done_nodes
    for nd in sorted(nodes, key=lambda n: n["order"]):
        if nxt is None and nd["ladder"] and not nd["done"]:
            for x in nd["ladder"]:
                if x["status"] != "solved":
                    nxt = {"id": x["id"], "title": x["title"], "node": nd["id"], "nodeTitle": nd["title"], "order": nd["order"],
                           "teaches": x["teaches"]}
                    break
    return {"phases": data.get("phases", {}), "nodes": nodes, "next": nxt, "total": total, "solved": solved_all}


def position(pid: str, bank=None) -> dict | None:
    _load()
    w = _cache["where"].get(pid)
    if not w:
        return None
    seq, i = w["seq"], w["index"]

    def peek(j):
        if 0 <= j < len(seq):
            d = bank.detail(seq[j]) if bank is not None else None
            return {"id": seq[j], "title": (d or {}).get("title") or seq[j]}
        return None
    return {"node": w["node"], "title": w["title"], "number": w["order"], "index": i, "total": len(seq),
            "teaches": w["teaches"], "level": w["level"], "prev": peek(i - 1), "next": peek(i + 1),
            # kept for the old path bar
            "inPlan": True, "planSize": len(seq)}
