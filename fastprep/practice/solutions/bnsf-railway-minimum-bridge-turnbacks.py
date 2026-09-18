# Longest-valid-subsequence DP with a Fenwick tree for prefix maxima over compressed weights.
from typing import List, Optional, Any
from bisect import bisect_right


def solution(U: int, weight: List[int]) -> int:
    n = len(weight)
    usable = [w for w in weight if w <= U]
    if not usable:
        return n
    vals = sorted(set(usable))
    m = len(vals)
    tree = [0] * (m + 1)

    def update(i, v):          # i is 1-based; prefix-max Fenwick
        while i <= m:
            if tree[i] < v:
                tree[i] = v
            i += i & (-i)

    def query(i):              # max over positions 1..i
        best = 0
        while i > 0:
            if tree[i] > best:
                best = tree[i]
            i -= i & (-i)
        return best

    best_overall = 0
    for w in weight:
        if w > U:
            continue
        # predecessors must weigh at most U - w
        k = bisect_right(vals, U - w)
        cur = query(k) + 1
        if cur > best_overall:
            best_overall = cur
        pos = bisect_right(vals, w)      # exact index of w (vals is sorted, w present)
        update(pos, cur)
    return n - best_overall
