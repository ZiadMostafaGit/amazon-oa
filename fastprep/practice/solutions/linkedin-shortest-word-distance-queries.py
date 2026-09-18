# Precompute index lists per word; per query binary-search the smaller list into the larger, with memoization.
from bisect import bisect_left
from typing import Dict, List


def shortestWordDistances(words: List[str], queries: List[List[str]]) -> List[int]:
    positions: Dict[str, List[int]] = {}
    for i, w in enumerate(words):
        positions.setdefault(w, []).append(i)

    cache: Dict[tuple, int] = {}
    out: List[int] = []
    for q in queries:
        a, b = q[0], q[1]
        key = (a, b) if a <= b else (b, a)
        hit = cache.get(key)
        if hit is not None:
            out.append(hit)
            continue
        pa = positions.get(a, [])
        pb = positions.get(b, [])
        if not pa or not pb:
            cache[key] = -1
            out.append(-1)
            continue
        if len(pa) > len(pb):
            pa, pb = pb, pa
        best = float('inf')
        for x in pa:
            j = bisect_left(pb, x)
            if j < len(pb):
                d = pb[j] - x
                if d < best:
                    best = d
            if j > 0:
                d = x - pb[j - 1]
                if d < best:
                    best = d
            if best == 1:
                break
        best = int(best)
        cache[key] = best
        out.append(best)
    return out
