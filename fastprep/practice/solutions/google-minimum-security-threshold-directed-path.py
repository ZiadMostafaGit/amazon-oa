from typing import List, Optional, Any
import heapq


def solve(n: int, edges: List[List[int]], source: int, target: int) -> int:
    # An edge with security s is usable when s < S, so the answer is
    # (minimum over paths of the maximum edge security) + 1.
    # Dijkstra with "max edge so far" as the relaxation key.
    if source == target:
        return 0

    adj = [[] for _ in range(n)]
    for e in edges:
        u, v, w = e[0], e[1], e[2]
        adj[u].append((v, w))

    INF = float('inf')
    best = [INF] * n
    best[source] = 0
    heap = [(0, source)]
    while heap:
        cur, u = heapq.heappop(heap)
        if cur > best[u]:
            continue
        if u == target:
            return cur + 1
        for v, w in adj[u]:
            nxt = cur if cur > w else w
            if nxt < best[v]:
                best[v] = nxt
                heapq.heappush(heap, (nxt, v))

    return -1
