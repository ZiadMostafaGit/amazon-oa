#!/usr/bin/env python3
"""Pick the problems worth a reference solution: the most repeated and the most recent.

"Top N" blends two rankings rather than choosing between them, because they
disagree: the most-repeated problems skew older, the newest sightings are
mostly seen once. Interleaving A (by seen_count) and B (by last_seen_max)
guarantees both ends are covered, and the blend is written into the manifest so
the choice is auditable.

    python3 tools/pick.py [N]        # default 1500 -> solutions/MANIFEST.json
"""
import json, os, sys

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, HERE)
import fpdb

OUT = os.path.join(HERE, "solutions", "MANIFEST.json")


def main(n: int = 1500) -> int:
    bank = fpdb.Bank()
    rows = [dict(r) for r in bank.conn.execute(
        "SELECT id, title, company, difficulty, practice_format, seen_count, "
        "last_seen_max, problem_types FROM problems")]

    by_seen = sorted(rows, key=lambda r: (-(r["seen_count"] or 0),
                                          r["last_seen_max"] or "", r["id"]), reverse=False)
    by_date = sorted(rows, key=lambda r: ((r["last_seen_max"] or ""), (r["seen_count"] or 0)),
                     reverse=True)

    picked, seen_ids = [], set()
    for i in range(max(len(by_seen), len(by_date))):
        for src, why in ((by_seen, "repeats"), (by_date, "recent")):
            if i < len(src) and len(picked) < n:
                r = src[i]
                if r["id"] in seen_ids:
                    continue
                seen_ids.add(r["id"])
                picked.append({"id": r["id"], "title": r["title"], "company": r["company"],
                               "difficulty": r["difficulty"], "format": r["practice_format"],
                               "seenCount": r["seen_count"] or 0,
                               "lastSeen": r["last_seen_max"],
                               "stages": json.loads(r["problem_types"] or "[]"),
                               "picked": why})
        if len(picked) >= n:
            break

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w") as f:
        json.dump({"count": len(picked), "problems": picked}, f, indent=1)

    algo = sum(1 for p in picked if p["format"] == "algorithm")
    print("%d problems -> %s" % (len(picked), OUT))
    print("  algorithm %d, tabular %d" % (algo, len(picked) - algo))
    print("  seen_count: min %d, max %d" % (min(p["seenCount"] for p in picked),
                                            max(p["seenCount"] for p in picked)))
    print("  newest %s, oldest %s" % (max(p["lastSeen"] or "" for p in picked),
                                      min(p["lastSeen"] or "" for p in picked)))
    print("  reached by repeats %d, by recency %d"
          % (sum(1 for p in picked if p["picked"] == "repeats"),
             sum(1 for p in picked if p["picked"] == "recent")))
    return 0


if __name__ == "__main__":
    sys.exit(main(int(sys.argv[1]) if len(sys.argv) > 1 else 1500))
