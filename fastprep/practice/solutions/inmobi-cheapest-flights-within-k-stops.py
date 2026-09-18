# Bellman-Ford relaxed exactly k+1 rounds using the previous round's distances.
from typing import List, Optional, Any


def findCheapestPrice(n: int, flights: List[List[int]], src: int, dst: int, k: int) -> int:
    INF = float("inf")
    dist = [INF] * n
    dist[src] = 0
    for _ in range(k + 1):
        prev = dist[:]
        for u, v, w in flights:
            if prev[u] + w < dist[v]:
                dist[v] = prev[u] + w
    return -1 if dist[dst] == INF else int(dist[dst])
