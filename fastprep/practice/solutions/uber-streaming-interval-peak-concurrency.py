# Compress endpoints into elementary segments; each arrival is a range +1 on [start, end) and the answer is the
# global maximum, kept by a lazy segment tree (mx[node] = max of children + pending add on the node).
from bisect import bisect_left
from typing import List


def peakConcurrencyAfterEachInsert(intervals: List[List[int]]) -> List[int]:
    xs = sorted({x for s, e in intervals for x in (s, e)})
    m = max(1, len(xs) - 1)              # elementary segments [xs[i], xs[i+1])
    mx = [0] * (4 * m)
    add = [0] * (4 * m)

    def update(node, lo, hi, l, r):
        if r < lo or hi < l:
            return
        if l <= lo and hi <= r:
            mx[node] += 1
            add[node] += 1
            return
        mid = (lo + hi) // 2
        update(2 * node, lo, mid, l, r)
        update(2 * node + 1, mid + 1, hi, l, r)
        mx[node] = max(mx[2 * node], mx[2 * node + 1]) + add[node]

    out = []
    for s, e in intervals:
        l, r = bisect_left(xs, s), bisect_left(xs, e) - 1
        update(1, 0, m - 1, l, r)
        out.append(mx[1])
    return out
