# Dijkstra with a binary heap over an adjacency list, -1 for unreachable vertices.
from typing import List, Optional, Any
import heapq


def shortestUndirectedDistances(vertexCount: int, edges: List[List[int]], source: int) -> List[int]:
    adj = [[] for _ in range(vertexCount)]
    for edge in edges:
        u, v, w = edge[0], edge[1], edge[2]
        adj[u].append((v, w))
        if u != v:
            adj[v].append((u, w))

    INF = float('inf')
    dist = [INF] * vertexCount
    dist[source] = 0
    heap = [(0, source)]
    while heap:
        d, node = heapq.heappop(heap)
        if d > dist[node]:
            continue
        for nxt, w in adj[node]:
            nd = d + w
            if nd < dist[nxt]:
                dist[nxt] = nd
                heapq.heappush(heap, (nd, nxt))
    return [-1 if d == INF else d for d in dist]
