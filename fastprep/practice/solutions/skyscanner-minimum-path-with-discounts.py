# Dijkstra over states (node, discounts used) with each edge relaxed at full price and at half price.
from typing import List, Optional, Any
import heapq


def minimumPathWithDiscounts(n: int, edges: List[List[int]], discounts: int) -> int:
    adj = [[] for _ in range(n)]
    for e in edges:
        u, v, w = e[0], e[1], e[2]
        adj[u].append((v, w))
        adj[v].append((u, w))

    INF = float('inf')
    dist = [[INF] * (discounts + 1) for _ in range(n)]
    dist[0][0] = 0
    pq = [(0, 0, 0)]  # cost, node, used discounts
    while pq:
        d, u, k = heapq.heappop(pq)
        if d > dist[u][k]:
            continue
        if u == n - 1:
            return d
        for v, w in adj[u]:
            nd = d + w
            if nd < dist[v][k]:
                dist[v][k] = nd
                heapq.heappush(pq, (nd, v, k))
            if k < discounts:
                nd2 = d + w // 2
                if nd2 < dist[v][k + 1]:
                    dist[v][k + 1] = nd2
                    heapq.heappush(pq, (nd2, v, k + 1))
    best = min(dist[n - 1])
    return -1 if best == INF else best
