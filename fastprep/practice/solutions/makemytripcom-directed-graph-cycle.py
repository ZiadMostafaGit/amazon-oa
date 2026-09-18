# Kahn's topological sort: a cycle exists when fewer than n vertices can be peeled off.
from typing import List, Optional, Any
from collections import deque


def hasDirectedCycle(n: int, edges: List[List[int]]) -> bool:
    adj = [[] for _ in range(n)]
    indeg = [0] * n
    for e in edges:
        u, v = e[0], e[1]
        adj[u].append(v)
        indeg[v] += 1

    queue = deque(i for i in range(n) if indeg[i] == 0)
    seen = 0
    while queue:
        u = queue.popleft()
        seen += 1
        for v in adj[u]:
            indeg[v] -= 1
            if indeg[v] == 0:
                queue.append(v)
    return seen != n
