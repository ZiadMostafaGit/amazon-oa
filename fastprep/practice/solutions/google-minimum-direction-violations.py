from typing import List, Optional, Any
from collections import deque


def minimumDirectionViolations(n: int, edges: List[List[int]], start: int, end: int) -> int:
    adj = [[] for _ in range(n)]
    for u, v in edges:
        adj[u].append((v, 0))  # along the arrow: free
        adj[v].append((u, 1))  # against the arrow: one violation
    INF = float("inf")
    dist = [INF] * n
    dist[start] = 0
    dq = deque([start])
    while dq:
        u = dq.popleft()
        for v, w in adj[u]:
            nd = dist[u] + w
            if nd < dist[v]:
                dist[v] = nd
                if w == 0:
                    dq.appendleft(v)
                else:
                    dq.append(v)
    return dist[end] if dist[end] < INF else -1
