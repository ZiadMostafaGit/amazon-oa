#!/usr/bin/env python3
"""Print the problem ids for one batch of the manifest.

    python3 tools/batch.py <batch-number>     # 0-based, BATCH problems each

Deterministic: batch n is always manifest[n*BATCH:(n+1)*BATCH], whatever has
been solved since. Solution-writing agents call this instead of being handed a
list, which keeps the orchestration args small and makes any batch re-runnable.
Already-solved problems are marked so an agent can skip them.
"""
import json, os, sys

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BATCH = 6


def main(n: int) -> int:
    man = json.load(open(os.path.join(HERE, "solutions", "MANIFEST.json")))["problems"]
    lo, hi = n * BATCH, (n + 1) * BATCH
    if lo >= len(man):
        print("(batch %d is past the end of the manifest: %d problems)" % (n, len(man)),
              file=sys.stderr)
        return 1
    try:
        index = json.load(open(os.path.join(HERE, "solutions", "VERIFIED.json")))["problems"]
    except (FileNotFoundError, json.JSONDecodeError, KeyError):
        index = {}
    for p in man[lo:hi]:
        ext = ".sql" if p["format"] == "tabular" else ".py"
        path = os.path.join(HERE, "solutions", p["id"] + ext)
        if os.path.exists(path) and (index.get(p["id"]) or {}).get("ok"):
            state = "DONE (verified; skip it)"
        elif os.path.exists(path):
            state = "has an unverified file (check it, fix or replace)"
        else:
            state = "TODO"
        print("%-58s %-9s %s" % (p["id"], p["format"], state))
    return 0


if __name__ == "__main__":
    sys.exit(main(int(sys.argv[1])) if len(sys.argv) > 1 else 2)
