# BFS from the source for shortest hop counts, then order nodes by (distance, id).
from typing import List, Optional, Any
from collections import deque


def recoverNetwork(networkNodes: int, networkFrom: List[int], networkTo: List[int], company: int) -> List[int]:
    adj = [[] for _ in range(networkNodes + 1)]
    for a, b in zip(networkFrom, networkTo):
        adj[a].append(b)
        adj[b].append(a)

    INF = -1
    dist = [INF] * (networkNodes + 1)
    dist[company] = 0
    q = deque([company])
    reached = []
    while q:
        u = q.popleft()
        for v in adj[u]:
            if dist[v] == INF:
                dist[v] = dist[u] + 1
                reached.append(v)
                q.append(v)

    reached.sort(key=lambda x: (dist[x], x))
    return reached
