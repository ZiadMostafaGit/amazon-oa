# BFS over reverse-dependency graph (flightTo -> flightFrom) from initially delayed flights.
from typing import List, Optional, Any
from collections import deque


def propagateFlightDelays(flightNodes: int, flightFrom: List[int], flightTo: List[int], delayed: List[int]) -> List[int]:
    adj = [[] for _ in range(flightNodes + 1)]
    for a, b in zip(flightFrom, flightTo):
        adj[b].append(a)
    seen = [False] * (flightNodes + 1)
    q = deque()
    for d in delayed:
        if not seen[d]:
            seen[d] = True
            q.append(d)
    while q:
        u = q.popleft()
        for v in adj[u]:
            if not seen[v]:
                seen[v] = True
                q.append(v)
    return [i for i in range(1, flightNodes + 1) if seen[i]]
