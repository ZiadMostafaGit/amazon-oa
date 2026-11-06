from typing import List, Optional, Any
from collections import deque


def minTeleporterRepairs(n: int, connections: List[List[int]], broken: List[int], source: int, destination: int) -> int:
    if source == destination:
        return 0
    is_broken = [0] * n
    for b in broken:
        is_broken[b] = 1
    adj = [[] for _ in range(n)]
    for a, b in connections:
        adj[a].append(b)
    INF = float("inf")
    dist = [INF] * n
    dist[source] = 0
    dq = deque([source])
    while dq:
        u = dq.popleft()
        w = is_broken[u]  # leaving a broken country costs one repair day
        for v in adj[u]:
            nd = dist[u] + w
            if nd < dist[v]:
                dist[v] = nd
                if w == 0:
                    dq.appendleft(v)
                else:
                    dq.append(v)
    return dist[destination] if dist[destination] < INF else -1
