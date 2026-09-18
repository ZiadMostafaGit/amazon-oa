#!/usr/bin/env python3
"""Everything an author needs before writing one chapter.

    python3 tools/brief_topic.py monotonic-stack
    python3 tools/brief_topic.py monotonic-stack --statements 3

Prints the topic's place in the canon, what it must also cover, its neighbours,
and a sample of the problems in this bank that practise it - so the chapter can
say "here, this shows up as ..." instead of guessing.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import textwrap

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, ROOT)
sys.path.insert(0, HERE)

import topics as topics_mod                                    # noqa: E402
from fpdb import Bank, html_to_text                            # noqa: E402


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("slug")
    ap.add_argument("--problems", type=int, default=25)
    ap.add_argument("--statements", type=int, default=2,
                    help="how many full statements to print")
    a = ap.parse_args()

    idx = topics_mod.index()
    t = idx["bySlug"].get(a.slug)
    if not t:
        print("no topic %r. Try: python3 tools/canon.py" % a.slug)
        return 1
    bank = Bank()

    print("=" * 72)
    print("%s   (%s)" % (t["title"], a.slug))
    print("=" * 72)
    print("category   : %s" % t["category"])
    print("rank       : #%d of %d, by how many problems here use it" % (t["rank"], len(idx["topics"])))
    print("problems   : %d%s" % (t["count"], "   <-- RARE: say so in the chapter"
                                 if t["rare"] else ""))
    print("kind       : %s" % t.get("kind", "topic"))
    if t.get("covers"):
        print("must also cover (folded into this chapter):")
        for c in t["covers"]:
            print("   - %s" % c)
    if t["needs"]:
        print("prerequisites (link with [[slug]]): %s" % ", ".join(t["needs"]))
    if t["near"]:
        print("read next     (link with [[slug]]): %s" % ", ".join(t["near"]))

    ids = (t.get("problems") or [])[:a.problems]
    if not ids:
        print("\nNo problem in the bank practises this. The chapter must open by "
              "saying so plainly, teach it anyway, and point at where it does "
              "appear in interviews elsewhere.")
        return 0

    print("\nproblems in this bank (easiest first, %d of %d):" % (len(ids), t["count"]))
    rows = {r["id"]: r for r in bank.query({"ids": ids}, sort="default",
                                           limit=len(ids))["items"]}
    for i in ids:
        r = rows.get(i)
        if not r:
            continue
        print("  %-9s %-52s %s" % (r["difficulty"] or "?", r["title"][:52], r["company"] or ""))

    for i in ids[:a.statements]:
        d = bank.detail(i)
        if not d:
            continue
        print("\n" + "-" * 72)
        print("FULL STATEMENT: %s  (%s)" % (d.get("title"), i))
        print("-" * 72)
        body = html_to_text(d.get("problemStatement") or "")
        print(textwrap.fill(body[:2200], 78))
        if d.get("constraints"):
            print("\nconstraints: " + textwrap.fill(
                html_to_text(d["constraints"])[:600], 78))
    return 0


if __name__ == "__main__":
    sys.exit(main())
