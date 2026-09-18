# Max-fuel Dijkstra from home (refueling resets the tank to L) plus multi-source Dijkstra to the nearest gas station for the return trip.
import heapq
from typing import List, Optional, Any


def computeNumberOfLocations(N: int, M: int, L: int, g: List[int], roads: List[List[int]]) -> int:
    if N <= 0:
        return 0

    gas = [0] * (N + 1)
    if len(g) == N + 1:
        # 1-indexed with a dummy leading entry
        for i in range(1, N + 1):
            gas[i] = 1 if g[i] else 0
    else:
        for i in range(1, N + 1):
            gas[i] = 1 if (i - 1 < len(g) and g[i - 1]) else 0
    gas[1] = 1  # home always has a gas station

    adj = [[] for _ in range(N + 1)]
    for row in roads:
        if not row or len(row) < 2:
            continue
        u, v = row[0], row[1]
        d = row[2] if len(row) >= 3 else 1
        if not (1 <= u <= N and 1 <= v <= N):
            continue
        adj[u].append((v, d))
        adj[v].append((u, d))

    # fuel[v] = maximum fuel that can remain while standing at v (-1 = unreachable)
    fuel = [-1] * (N + 1)
    fuel[1] = L
    pq = [(-L, 1)]
    while pq:
        nf, u = heapq.heappop(pq)
        f = -nf
        if f < fuel[u]:
            continue
        for v, d in adj[u]:
            r = f - d
            if r < 0:
                continue
            if gas[v]:
                r = L
            if r > fuel[v]:
                fuel[v] = r
                heapq.heappush(pq, (-r, v))

    # shortest distance from each node to the nearest gas station (the way back)
    INF = float('inf')
    back = [INF] * (N + 1)
    pq2 = []
    for i in range(1, N + 1):
        if gas[i]:
            back[i] = 0
            pq2.append((0, i))
    heapq.heapify(pq2)
    while pq2:
        dd, u = heapq.heappop(pq2)
        if dd > back[u]:
            continue
        for v, d in adj[u]:
            nd = dd + d
            if nd < back[v]:
                back[v] = nd
                heapq.heappush(pq2, (nd, v))

    count = 0
    for v in range(1, N + 1):
        if fuel[v] >= 0 and back[v] <= fuel[v]:
            count += 1
    return count
