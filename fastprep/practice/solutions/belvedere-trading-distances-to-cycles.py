from typing import List, Optional, Any
from collections import deque


def distancesToCycles(n: int, edges: List[List[int]]) -> List[int]:
    adj = [[] for _ in range(n)]
    deg = [0] * n
    for u, v in edges:
        adj[u].append(v)
        adj[v].append(u)
        deg[u] += 1
        deg[v] += 1
    # peel leaves: whatever is never peeled lies on a cycle
    removed = [False] * n
    q = deque(i for i in range(n) if deg[i] == 1)
    while q:
        u = q.popleft()
        removed[u] = True
        for v in adj[u]:
            if not removed[v]:
                deg[v] -= 1
                if deg[v] == 1:
                    q.append(v)
    dist = [-1] * n
    q = deque()
    for i in range(n):
        if not removed[i]:
            dist[i] = 0
            q.append(i)
    while q:
        u = q.popleft()
        for v in adj[u]:
            if dist[v] == -1:
                dist[v] = dist[u] + 1
                q.append(v)
    return dist
