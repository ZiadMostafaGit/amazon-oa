# Sliding insertion into a Fenwick tree over compressed heights; predecessor/successor queries by binary lifting.
from typing import List, Optional, Any


def minimumPeakHeightDifference(heights: List[int], viewingGap: int) -> int:
    n = len(heights)
    if viewingGap >= n:
        return -1
    vals = sorted(set(heights))
    m = len(vals)
    rank = {v: i + 1 for i, v in enumerate(vals)}
    tree = [0] * (m + 1)

    LOG = 1
    while (1 << LOG) <= m:
        LOG += 1
    LOG -= 1

    def add(i: int) -> None:
        while i <= m:
            tree[i] += 1
            i += i & (-i)

    def prefix(i: int) -> int:
        s = 0
        while i > 0:
            s += tree[i]
            i -= i & (-i)
        return s

    def kth(k: int) -> int:
        # smallest index with prefix >= k, or 0 if none
        pos = 0
        rem = k
        step = 1 << LOG
        while step:
            nxt = pos + step
            if nxt <= m and tree[nxt] < rem:
                pos = nxt
                rem -= tree[pos]
            step >>= 1
        return pos + 1 if pos + 1 <= m else 0

    best = None
    total = 0
    for b in range(viewingGap, n):
        v = heights[b - viewingGap]
        add(rank[v])
        total += 1
        x = heights[b]
        rx = rank[x]
        c = prefix(rx)
        if c > 0:
            p = kth(c)
            if p:
                d = x - vals[p - 1]
                if best is None or d < best:
                    best = d
                    if best == 0:
                        return 0
        if c < total:
            s = kth(c + 1)
            if s:
                d = vals[s - 1] - x
                if best is None or d < best:
                    best = d
                    if best == 0:
                        return 0
    return best if best is not None else -1
