# BFS for the fewest-edge path plus Dijkstra for the minimum-weight path.
import heapq
from typing import List, Optional, Any
from collections import deque


def shortestDistances(matrix: List[List[int]], source: int, target: int) -> List[int]:
    n = len(matrix)
    if source == target:
        return [0, 0]

    adj = [[] for _ in range(n)]
    for u in range(n):
        row = matrix[u]
        for v in range(n):
            if u != v and row[v] > 0:
                adj[u].append((v, row[v]))

    # fewest edges
    INF = float('inf')
    hops = [-1] * n
    hops[source] = 0
    q = deque([source])
    while q:
        u = q.popleft()
        for v, _w in adj[u]:
            if hops[v] == -1:
                hops[v] = hops[u] + 1
                q.append(v)

    # least total weight
    dist = [INF] * n
    dist[source] = 0
    pq = [(0, source)]
    while pq:
        d, u = heapq.heappop(pq)
        if d > dist[u]:
            continue
        if u == target:
            break
        for v, w in adj[u]:
            nd = d + w
            if nd < dist[v]:
                dist[v] = nd
                heapq.heappush(pq, (nd, v))

    return [hops[target], dist[target]]
