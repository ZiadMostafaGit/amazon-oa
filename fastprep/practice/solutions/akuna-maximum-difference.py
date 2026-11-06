# Union-find; each root tracks its component's min and max label.
from typing import List, Optional, Any


def maximumDifference(g_nodes: int, g_from: List[int], g_to: List[int]) -> int:
    parent = list(range(g_nodes + 1))
    lo = list(range(g_nodes + 1))
    hi = list(range(g_nodes + 1))

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    for a, b in zip(g_from, g_to):
        ra, rb = find(a), find(b)
        if ra != rb:
            parent[ra] = rb
            if lo[ra] < lo[rb]:
                lo[rb] = lo[ra]
            if hi[ra] > hi[rb]:
                hi[rb] = hi[ra]
    best = 0
    for v in range(1, g_nodes + 1):
        if parent[v] == v and hi[v] - lo[v] > best:
            best = hi[v] - lo[v]
    return best
