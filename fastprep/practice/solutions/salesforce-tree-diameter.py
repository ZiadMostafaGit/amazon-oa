# Double BFS: farthest vertex from node 0, then farthest distance from that vertex.
from collections import deque
from typing import List


def treeDiameter(n: int, edges: List[List[int]]) -> int:
    if n <= 1:
        return 0
    adj = [[] for _ in range(n)]
    for u, v in edges:
        adj[u].append(v)
        adj[v].append(u)

    def bfs(src: int):
        dist = [-1] * n
        dist[src] = 0
        q = deque([src])
        far, fard = src, 0
        while q:
            cur = q.popleft()
            for nxt in adj[cur]:
                if dist[nxt] == -1:
                    dist[nxt] = dist[cur] + 1
                    if dist[nxt] > fard:
                        fard = dist[nxt]
                        far = nxt
                    q.append(nxt)
        return far, fard

    a, _ = bfs(0)
    _, d = bfs(a)
    return d
