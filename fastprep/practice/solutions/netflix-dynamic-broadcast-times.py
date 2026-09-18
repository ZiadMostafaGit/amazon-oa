# Dijkstra per query over a mutable weight array, with a cache invalidated on each update.
from typing import List, Optional, Any
import heapq


def processBroadcastOperations(n: int, edges: List[List[int]], operations: List[List[int]]) -> List[List[int]]:
    weights = [e[2] for e in edges]
    # adjacency: node -> list of (neighbor, edge_index)
    adj = [[] for _ in range(n)]
    for i, e in enumerate(edges):
        adj[e[0]].append((e[1], i))

    INF = float('inf')
    cache = {}
    results = []

    for op in operations:
        if op[0] == 0:
            idx, w = op[1], op[2]
            if weights[idx] != w:
                weights[idx] = w
                cache.clear()
        else:
            src = op[1]
            hit = cache.get(src)
            if hit is None:
                dist = [INF] * n
                dist[src] = 0
                pq = [(0, src)]
                while pq:
                    d, u = heapq.heappop(pq)
                    if d > dist[u]:
                        continue
                    for v, ei in adj[u]:
                        nd = d + weights[ei]
                        if nd < dist[v]:
                            dist[v] = nd
                            heapq.heappush(pq, (nd, v))
                hit = [-1 if x == INF else x for x in dist]
                cache[src] = hit
            results.append(list(hit))

    return results
