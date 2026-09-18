# Sorted list (bisect insort) of distinct words; a prefix search scans forward from the lower bound.
from bisect import bisect_left, insort
from typing import List


def solve(operations: List[str]) -> List[List[str]]:
    words = []
    seen = set()
    res = []
    for op in operations:
        parts = op.split(None, 1)
        if not parts:
            continue
        cmd = parts[0].upper()
        arg = parts[1].strip() if len(parts) > 1 else ""
        if cmd == "INSERT":
            if arg not in seen:
                seen.add(arg)
                insort(words, arg)
        else:
            i = bisect_left(words, arg)
            hit = []
            while i < len(words) and len(hit) < 3 and words[i].startswith(arg):
                hit.append(words[i])
                i += 1
            res.append(hit)
    return res
