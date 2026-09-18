# Three BFS passes from x, y, z, then check the sorted distance triple at every vertex.
from typing import List, Optional, Any
from collections import deque


def countPythagoreanVertices(n: int, edges: List[List[int]], x: int, y: int, z: int) -> int:
    adj = [[] for _ in range(n + 1)]
    for u, v in edges:
        adj[u].append(v)
        adj[v].append(u)

    def bfs(src: int) -> List[int]:
        dist = [-1] * (n + 1)
        dist[src] = 0
        q = deque([src])
        while q:
            u = q.popleft()
            for w in adj[u]:
                if dist[w] < 0:
                    dist[w] = dist[u] + 1
                    q.append(w)
        return dist

    dx, dy, dz = bfs(x), bfs(y), bfs(z)
    count = 0
    for v in range(1, n + 1):
        a, b, c = sorted((dx[v], dy[v], dz[v]))
        if a > 0 and a * a + b * b == c * c:
            count += 1
    return count
