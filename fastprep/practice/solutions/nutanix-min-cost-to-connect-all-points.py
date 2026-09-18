# Prim's minimum spanning tree on the dense Manhattan-distance graph, O(n^2).
from typing import List, Optional, Any


def minCostConnectPoints(points: List[List[int]]) -> int:
    n = len(points)
    if n <= 1:
        return 0
    INF = float('inf')
    best = [INF] * n
    used = [False] * n
    best[0] = 0
    total = 0
    for _ in range(n):
        u = -1
        bu = INF
        for i in range(n):
            if not used[i] and best[i] < bu:
                bu = best[i]
                u = i
        used[u] = True
        total += bu
        xu, yu = points[u]
        for v in range(n):
            if not used[v]:
                xv, yv = points[v]
                d = abs(xu - xv) + abs(yu - yv)
                if d < best[v]:
                    best[v] = d
    return total
