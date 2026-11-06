from typing import List, Optional, Any
from collections import deque


def findMinDistanceToFurthestNode(n: int, edges: List[List[int]]) -> int:
    # min over x of eccentricity = tree radius = ceil(diameter / 2)
    adj = [[] for _ in range(n + 1)]
    for u, v in edges:
        adj[u].append(v)
        adj[v].append(u)

    def bfs(src):
        dist = [-1] * (n + 1)
        dist[src] = 0
        q = deque([src])
        far = src
        while q:
            u = q.popleft()
            if dist[u] > dist[far]:
                far = u
            for w in adj[u]:
                if dist[w] < 0:
                    dist[w] = dist[u] + 1
                    q.append(w)
        return far, dist[far]

    a, _ = bfs(1)
    _, diameter = bfs(a)
    return (diameter + 1) // 2
