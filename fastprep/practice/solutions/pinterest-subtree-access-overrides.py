# Euler-tour ranges + segment tree with timestamped range-assign tags, point query takes the newest tag on the root-to-leaf path.
from typing import List, Optional, Any


def resolveRegionAccess(parent: List[int], operations: List[str], regions: List[int]) -> List[bool]:
    n = len(parent)
    children = [[] for _ in range(n)]
    root = 0
    for v in range(n):
        p = parent[v]
        if p == -1:
            root = v
        else:
            children[p].append(v)

    tin = [0] * n
    tout = [0] * n
    timer = 0
    # iterative dfs producing contiguous subtree intervals
    stack = [(root, False)]
    while stack:
        node, processed = stack.pop()
        if processed:
            tout[node] = timer - 1
            continue
        tin[node] = timer
        timer += 1
        stack.append((node, True))
        for c in reversed(children[node]):
            stack.append((c, False))

    size = 1
    while size < n:
        size <<= 1
    # tag[i] = (stamp, value); stamp 0 means no assignment
    stamp = [0] * (2 * size)
    val = [False] * (2 * size)

    def assign(l: int, r: int, t: int, v: bool) -> None:
        lo = l + size
        hi = r + size + 1
        while lo < hi:
            if lo & 1:
                stamp[lo] = t
                val[lo] = v
                lo += 1
            if hi & 1:
                hi -= 1
                stamp[hi] = t
                val[hi] = v
            lo >>= 1
            hi >>= 1

    def query(pos: int) -> bool:
        i = pos + size
        best_t = 0
        best_v = False
        while i >= 1:
            if stamp[i] > best_t:
                best_t = stamp[i]
                best_v = val[i]
            i >>= 1
        return best_v

    res = []
    for i, op in enumerate(operations):
        node = regions[i]
        if op == "CHECK":
            res.append(query(tin[node]))
        else:
            assign(tin[node], tout[node], i + 1, op == "GRANT")
    return res
