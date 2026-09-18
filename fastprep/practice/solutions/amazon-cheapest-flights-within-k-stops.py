# Bellman-Ford relaxed exactly k+1 times (edge-limited shortest path).
from typing import List, Optional, Any


def solve(n: int, flights: List[List[int]], src: int, dst: int, k: int) -> int:
    INF = float('inf')
    dist = [INF] * n
    dist[src] = 0
    for _ in range(k + 1):
        nxt = dist[:]
        changed = False
        for u, v, w in flights:
            if dist[u] + w < nxt[v]:
                nxt[v] = dist[u] + w
                changed = True
        dist = nxt
        if not changed:
            break
    return -1 if dist[dst] == INF else dist[dst]
