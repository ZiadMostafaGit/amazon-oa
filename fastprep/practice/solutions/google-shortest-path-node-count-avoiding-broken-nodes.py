# BFS over the directed graph, skipping broken nodes; returns node count on the shortest path.
from collections import deque
from typing import List, Optional, Any


def minimumPathNodeCount(graph: List[List[int]], broken: List[int], start: int, destination: int) -> int:
    bad = set(broken)
    if start in bad or destination in bad:
        return -1
    if start == destination:
        return 1

    n = len(graph)
    dist = [-1] * n
    dist[start] = 1
    q = deque([start])
    while q:
        u = q.popleft()
        d = dist[u] + 1
        for v in graph[u]:
            if dist[v] == -1 and v not in bad:
                if v == destination:
                    return d
                dist[v] = d
                q.append(v)
    return -1
