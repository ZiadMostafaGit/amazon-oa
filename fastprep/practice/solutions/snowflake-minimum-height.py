# Approach: binary search the height, greedily cutting bottom-up any deep subtree that cannot stay attached.
from typing import List, Optional, Any


def getMinimumHeight(tree_nodes: int, tree_from: List[int], tree_to: List[int], max_operations: int) -> int:
    n = tree_nodes
    if n <= 1:
        return 0
    adj = [[] for _ in range(n + 1)]
    for a, b in zip(tree_from, tree_to):
        adj[a].append(b)
        adj[b].append(a)

    parent = [0] * (n + 1)
    order = []
    parent[1] = 0
    visited = [False] * (n + 1)
    visited[1] = True
    stack = [1]
    while stack:
        v = stack.pop()
        order.append(v)
        for w in adj[v]:
            if not visited[w]:
                visited[w] = True
                parent[w] = v
                stack.append(w)

    rev = order[::-1]

    def feasible(h: int) -> bool:
        if h < 1:
            return False
        d = [0] * (n + 1)
        used = 0
        for v in rev:
            if v == 1:
                continue
            p = parent[v]
            if p != 1 and d[v] + 2 > h:
                used += 1
                if used > max_operations:
                    return False
            else:
                if d[v] + 1 > d[p]:
                    d[p] = d[v] + 1
        return d[1] <= h

    lo, hi = 1, n - 1
    while lo < hi:
        mid = (lo + hi) // 2
        if feasible(mid):
            hi = mid
        else:
            lo = mid + 1
    return lo
