# Dijkstra with a binary heap over the adjacency list, then answer each target query.
import heapq
from typing import List, Optional, Any


def shortestPathsToTargets(n: int, edges: List[List[int]], source: int, targets: List[int]) -> List[int]:
    adj = [[] for _ in range(n + 1)]
    for e in edges:
        u, v, w = e[0], e[1], e[2]
        if 1 <= u <= n and 1 <= v <= n:
            adj[u].append((v, w))

    INF = float('inf')
    dist = [INF] * (n + 1)
    if 1 <= source <= n:
        dist[source] = 0
        heap = [(0, source)]
        while heap:
            d, u = heapq.heappop(heap)
            if d > dist[u]:
                continue
            for v, w in adj[u]:
                nd = d + w
                if nd < dist[v]:
                    dist[v] = nd
                    heapq.heappush(heap, (nd, v))

    out = []
    for t in targets:
        if 1 <= t <= n and dist[t] != INF:
            out.append(dist[t])
        else:
            out.append(-1)
    return out
