# Offline coordinate compression of every endpoint, then a segment tree over elementary segments with
# lazy range assignment (tracked = 1 / 0) and range-minimum queries (all tracked <=> min == 1).
from bisect import bisect_left
from typing import List


def rangeModule(operations: List[str], ranges: List[List[int]]) -> List[bool]:
    xs = sorted({x for l, r in ranges for x in (l, r)})
    m = max(1, len(xs) - 1)
    mn = [0] * (4 * m)
    lazy = [-1] * (4 * m)

    def push(node):
        v = lazy[node]
        if v != -1:
            for ch in (2 * node, 2 * node + 1):
                mn[ch] = v
                lazy[ch] = v
            lazy[node] = -1

    def assign(node, lo, hi, l, r, v):
        if r < lo or hi < l:
            return
        if l <= lo and hi <= r:
            mn[node] = v
            lazy[node] = v
            return
        push(node)
        mid = (lo + hi) // 2
        assign(2 * node, lo, mid, l, r, v)
        assign(2 * node + 1, mid + 1, hi, l, r, v)
        mn[node] = min(mn[2 * node], mn[2 * node + 1])

    def query(node, lo, hi, l, r):
        if r < lo or hi < l:
            return 1
        if l <= lo and hi <= r:
            return mn[node]
        push(node)
        mid = (lo + hi) // 2
        return min(query(2 * node, lo, mid, l, r), query(2 * node + 1, mid + 1, hi, l, r))

    out = []
    for op, (left, right) in zip(operations, ranges):
        l, r = bisect_left(xs, left), bisect_left(xs, right) - 1
        if op == "addRange":
            assign(1, 0, m - 1, l, r, 1)
        elif op == "removeRange":
            assign(1, 0, m - 1, l, r, 0)
        else:
            out.append(query(1, 0, m - 1, l, r) == 1)
    return out
