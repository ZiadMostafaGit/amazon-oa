# Dijkstra on a max-heap, relaxing by multiplying edge success probabilities.
from typing import List, Optional, Any
import heapq


def maxProbability(n: int, edges: List[List[int]], probabilities: List[float], start: int, end: int) -> float:
    if start == end:
        return 1.0
    adj = [[] for _ in range(n)]
    for (u, v), p in zip(edges, probabilities):
        adj[u].append((v, p))
        adj[v].append((u, p))

    best = [0.0] * n
    best[start] = 1.0
    heap = [(-1.0, start)]
    while heap:
        negp, u = heapq.heappop(heap)
        p = -negp
        if p < best[u]:
            continue
        if u == end:
            return p
        for v, w in adj[u]:
            np_ = p * w
            if np_ > best[v]:
                best[v] = np_
                heapq.heappush(heap, (-np_, v))
    return 0.0
