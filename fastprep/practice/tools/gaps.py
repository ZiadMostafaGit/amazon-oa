#!/usr/bin/env python3
"""What is missing, per problem, across the whole bank.

The bank is a scrape of reported problems, so it is uneven: some entries have
no constraints, a few have no worked explanation, some tabular ones publish a
single visible case. This prints that inventory so the gaps are known rather
than discovered one problem at a time - and the app shows the same facts on
the problem itself instead of rendering an empty section.

    python3 tools/gaps.py            # summary
    python3 tools/gaps.py --list X   # the ids missing X
"""
import collections, json, os, sys

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, HERE)
import fpdb, images, solutions


def gaps_for(d: dict) -> list:
    """The specific things this problem does not have."""
    out = []
    t = fpdb.html_to_text
    if not t(d.get("problemStatement") or "").strip():
        out.append("statement")
    if not t(d.get("constraints") or "").strip():
        out.append("constraints")
    if d.get("practiceFormat") == "tabular":
        tab = d.get("tabular") or {}
        if not (tab.get("visibleCases") or []):
            out.append("visible cases")
        if not (tab.get("inputSchema") or []):
            out.append("table schema")
        if not (tab.get("resultContract") or {}).get("columns"):
            out.append("result contract")
    else:
        examples = d.get("examples") or []
        if not examples:
            out.append("examples")
        elif len(examples) == 1:
            out.append("only one example")
        if not any((e.get("explanation") or "").strip() for e in examples):
            out.append("worked explanation")
        if not d.get("functionName"):
            out.append("function name")
        if not (d.get("starterCode") or "").strip():
            out.append("starter code")
    if not (d.get("topics") or []):
        out.append("topics")
    if not d.get("difficulty"):
        out.append("difficulty")
    if not (d.get("sourceImages") or []):
        out.append("source screenshots")
    return out


def main(argv) -> int:
    bank = fpdb.Bank()
    want = argv[1] if len(argv) > 1 and argv[0] == "--list" else None
    counts = collections.Counter()
    listed = []
    total = 0
    for r in bank.conn.execute("SELECT id FROM problems"):
        d = bank.detail(r["id"])
        total += 1
        g = gaps_for(d)
        for item in g:
            counts[item] += 1
        if want and want in g:
            listed.append(r["id"])

    if want:
        for pid in listed[:200]:
            print(pid)
        print("\n%d problem(s) missing %r" % (len(listed), want))
        return 0

    print("%d problems\n" % total)
    for item, n in counts.most_common():
        print("  %-22s missing in %5d  (%4.1f%%)" % (item, n, 100.0 * n / total))
    s = solutions.stats()
    print("\n  reference solution     stored for %d, verified %d (targeting %d)"
          % (s["stored"], s["verified"], s["targeted"]))
    print("  source screenshots     %d cached locally" % images.cached_count())
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
