# Approach: case analysis on the op budget - 1 op = smallest adjacent gap, 2 ops = nearest distance between all
# pairwise differences and the original values, 3+ ops = 0 (append the same difference twice, then subtract them).
from typing import List, Optional, Any
from bisect import bisect_left


def getMinimumValue(data: List[int], maxOperations: int) -> int:
    a = sorted(data)
    n = len(a)

    best = a[0]
    for i in range(1, n):
        g = a[i] - a[i - 1]
        if g < best:
            best = g
    if best == 0 or maxOperations >= 3:
        # two equal values (or a spare operation to create them) give an absolute difference of 0
        return 0
    if maxOperations == 1:
        return best

    # exactly two operations: first append some |a[i]-a[j]|, then pair it with an original value
    diffs: List[int] = []
    for i in range(n - 1):
        ai = a[i]
        diffs.extend([x - ai for x in a[i + 1:]])
    diffs.sort()

    for c in a:
        j = bisect_left(diffs, c)
        if j < len(diffs):
            d = diffs[j] - c
            if d < best:
                best = d
        if j > 0:
            d = c - diffs[j - 1]
            if d < best:
                best = d
        if best == 0:
            break
    return best
