from collections import deque
from typing import List


def minimumDiameter(n: int, k: int, edges: List[List[int]]) -> int:
    # Removing k leaves one by one can leave ANY connected subtree of m = n - k
    # nodes. A subtree of diameter D fits inside the ball of radius D//2 around
    # a centre node (D even) or a centre edge (D odd), and every ball can be
    # trimmed down to any smaller connected size, so we only need ball sizes.
    m = n - k
    if m <= 1:
        return 0
    adj = [[] for _ in range(n)]
    for u, v in edges:
        adj[u].append(v)
        adj[v].append(u)
    dist = []
    for s in range(n):
        d = [-1] * n
        d[s] = 0
        q = deque([s])
        while q:
            x = q.popleft()
            for y in adj[x]:
                if d[y] < 0:
                    d[y] = d[x] + 1
                    q.append(y)
        dist.append(d)
    best = n
    for s in range(n):
        r = sorted(dist[s])[m - 1]
        best = min(best, 2 * r)
    for u, v in edges:
        du, dv = dist[u], dist[v]
        r = sorted(min(a, b) for a, b in zip(du, dv))[m - 1]
        best = min(best, 2 * r + 1)
    return best
