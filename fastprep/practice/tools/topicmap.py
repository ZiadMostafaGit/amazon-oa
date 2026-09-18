#!/usr/bin/env python3
"""Map every problem in the bank onto the 150-topic canon.

Two signals, because neither alone is enough:

  * the bank's own `topics` array - accurate, but only 36 coarse names, and
    "stack" cannot tell you a problem wants a monotonic stack;
  * regexes over the title and the statement text - they see the vocabulary a
    statement uses ("next greater element", "minimise the maximum"), which is
    how a human recognises the pattern.

Each match carries a score, so a topic's practice queue starts with the
problems that are most clearly about it rather than whatever sorted first:

    tag match ....... 3
    title pattern ... 3   (a pattern in the title is a strong statement)
    body pattern .... 1   each distinct pattern, capped at 3

A problem shows at most TOP_PER_PROBLEM topic links, so the tags under a
statement stay meaningful; a topic's queue keeps every match.

Writes topics/INDEX.json. Read-only on the bank.
"""

from __future__ import annotations

import json
import os
import re
import sqlite3
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, ROOT)
sys.path.insert(0, HERE)

from fpdb import html_to_text                                 # noqa: E402
from canon import CANON                                       # noqa: E402

DB = os.path.abspath(os.path.join(ROOT, "..", "fastprep.db"))
OUT = os.path.join(ROOT, "topics", "INDEX.json")
TOP_PER_PROBLEM = 6
DIFF_ORDER = {"easy": 0, "medium": 1, "hard": 2}
# Chapters about method rather than about a family of problems. They keep no
# practice queue - you practise them on every problem - so they are neither
# ranked by count nor marked rare.
CRAFT = "Interview Craft"
# Chapters about how a family of problems is solved rather than about a family
# of their own. They inherit the parent's tag, so their queue is the parent's;
# they are ranked immediately after it instead of ahead of it on a stray match.
METHOD = {"memoization", "state-design", "greedy-exchange"}


def flags(pattern):
    """Case-insensitive, unless the pattern spells something in capitals.

    `\\bSELECT\\b` must not match the English word "select", and `\\bDP\\b` must
    not match "dp" inside a variable name; but `\\bsliding window\\b` should
    match however the statement capitalises it.
    """
    return 0 if any(c.isupper() for c in re.sub(r"\\[a-zA-Z]", "", pattern)) else re.I


def compiled():
    out = []
    for cat, slug, title, tags, pats, needs, near, covers in CANON:
        out.append({
            "category": cat, "slug": slug, "title": title,
            "tags": set(tags),
            "res": [re.compile(p, flags(p)) for p in pats],
            "needs": needs, "near": near, "covers": covers,
        })
    return out


def score(topic, problem_tags, title, body):
    s = 0
    why = []
    if topic["tags"] & problem_tags:
        s += 3
        why.append("tag")
    hits = 0
    for rx in topic["res"]:
        if rx.search(title):
            s += 3
            why.append("title")
            break
    for rx in topic["res"]:
        if rx.search(body):
            hits += 1
            if hits >= 3:
                break
    s += hits
    if hits:
        why.append("text")
    return s, why


def build(db_path=DB):
    con = sqlite3.connect("file:%s?mode=ro" % db_path, uri=True)
    con.execute("PRAGMA query_only = ON")
    topics = compiled()
    per_topic = {t["slug"]: [] for t in topics}
    by_problem = {}
    rows = con.execute(
        "SELECT id, title, topics, difficulty, detail_json FROM problems").fetchall()
    for pid, title, tags_json, difficulty, detail_json in rows:
        try:
            ptags = set(json.loads(tags_json or "[]"))
        except Exception:
            ptags = set()
        body = title or ""
        if detail_json:
            try:
                d = json.loads(detail_json)
                body += "\n" + html_to_text(d.get("problemStatement") or "")
                body += "\n" + html_to_text(d.get("constraints") or "")
                body += "\n" + (d.get("functionName") or "")
            except Exception:
                pass
        matches = []
        for t in topics:
            s, why = score(t, ptags, title or "",
                           "" if t["slug"] in METHOD else body)
            if s:
                matches.append((s, t["slug"]))
        matches.sort(key=lambda m: (-m[0], m[1]))
        rank = DIFF_ORDER.get(difficulty, 3)
        for s, slug in matches:
            per_topic[slug].append((-s, rank, title or "", pid))
        by_problem[pid] = [slug for _, slug in matches[:TOP_PER_PROBLEM]]
    con.close()

    out = []
    for t in topics:
        craft = t["category"] == CRAFT
        q = [] if craft else sorted(per_topic[t["slug"]])
        out.append({
            "slug": t["slug"], "title": t["title"], "category": t["category"],
            "needs": t["needs"], "near": t["near"], "covers": t["covers"],
            "kind": "craft" if craft else
                    ("method" if t["slug"] in METHOD else "topic"),
            "count": len(q),
            "rare": not craft and not q,
            # Easiest first - but a problem matched by one stray phrase is not
            # what you want at the top of a practice queue, so weak matches
            # (a single body pattern and nothing else) sink to the bottom.
            "problems": [pid for _, _, _, pid in
                         sorted(q, key=lambda r: (-r[0] < 3, r[1], r[0], r[2]))],
        })
    # craft chapters sit after the topics they apply to, in their own order
    out.sort(key=lambda t: (t["kind"] == "craft", -t["count"],
                            t["kind"] == "method", t["category"], t["title"]))
    for i, t in enumerate(out):
        t["rank"] = i + 1
    return {"problems": len(rows), "topics": out, "byProblem": by_problem}


def main():
    index = build()
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w") as fh:
        json.dump(index, fh, separators=(",", ":"))
    ts = index["topics"]
    rare = [t for t in ts if t["rare"]]
    print("%d problems -> %d topics, %d rare, %s"
          % (index["problems"], len(ts), len(rare),
             "%.1f topic links per problem" %
             (sum(len(v) for v in index["byProblem"].values()) / len(index["byProblem"]))))
    print("\ntop 25:")
    for t in ts[:25]:
        print("  %2d. %-34s %5d" % (t["rank"], t["slug"], t["count"]))
    print("\nrare (%d):" % len(rare))
    print("  " + ", ".join(t["slug"] for t in rare))
    print("\nthin (1-9 problems):")
    print("  " + ", ".join("%s(%d)" % (t["slug"], t["count"])
                           for t in ts if 0 < t["count"] < 10))


if __name__ == "__main__":
    main()
