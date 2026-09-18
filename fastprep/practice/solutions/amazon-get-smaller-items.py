# Difference array for per-item pick counts, then sort values with prefix sums and binary search per query.
from typing import List, Optional, Any
from bisect import bisect_left


def getSmallerItems(items: List[int], start: List[int], end: List[int], query: List[int]) -> List[int]:
    n = len(items)
    diff = [0] * (n + 1)
    for s, e in zip(start, end):
        diff[s] += 1
        diff[e + 1] -= 1

    counts = [0] * n
    run = 0
    for i in range(n):
        run += diff[i]
        counts[i] = run

    pairs = sorted(zip(items, counts))
    values = [v for v, _ in pairs]
    prefix = [0] * (n + 1)
    for i, (_, c) in enumerate(pairs):
        prefix[i + 1] = prefix[i] + c

    return [prefix[bisect_left(values, q)] for q in query]
