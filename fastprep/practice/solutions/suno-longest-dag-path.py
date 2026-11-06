from typing import List, Optional, Any
from collections import deque


def longestDagPath(n: int, edges: List[List[int]]) -> int:
    adj = [[] for _ in range(n)]
    indeg = [0] * n
    for u, v in edges:
        adj[u].append(v)
        indeg[v] += 1
    longest = [0] * n  # most edges on a path ending at this node
    q = deque(i for i in range(n) if indeg[i] == 0)
    while q:
        u = q.popleft()
        for v in adj[u]:
            if longest[u] + 1 > longest[v]:
                longest[v] = longest[u] + 1
            indeg[v] -= 1
            if indeg[v] == 0:
                q.append(v)
    return max(longest) if n else 0
