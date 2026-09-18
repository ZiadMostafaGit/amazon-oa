# BFS from source over an adjacency list, returning the level at which target is reached.
from collections import deque
from typing import List


def shortestPathLength(n: int, edges: List[List[int]], source: int, target: int) -> int:
    if source == target:
        return 0
    adj = [[] for _ in range(n)]
    for u, v in edges:
        adj[u].append(v)
        adj[v].append(u)
    dist = [-1] * n
    dist[source] = 0
    q = deque([source])
    while q:
        u = q.popleft()
        du = dist[u]
        for w in adj[u]:
            if dist[w] == -1:
                dist[w] = du + 1
                if w == target:
                    return du + 1
                q.append(w)
    return -1
