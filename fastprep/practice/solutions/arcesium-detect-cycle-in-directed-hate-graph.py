# Kahn topological sort: a directed cycle exists iff some node is never dequeued.
from typing import List, Optional, Any
from collections import deque


def hasDirectedHateCycle(n: int, hatePairs: List[List[int]]) -> bool:
    adj = [[] for _ in range(n)]
    indeg = [0] * n
    for pair in hatePairs:
        u, v = pair[0], pair[1]
        adj[u].append(v)
        indeg[v] += 1
    q = deque(i for i in range(n) if indeg[i] == 0)
    seen = 0
    while q:
        u = q.popleft()
        seen += 1
        for v in adj[u]:
            indeg[v] -= 1
            if indeg[v] == 0:
                q.append(v)
    return seen != n
