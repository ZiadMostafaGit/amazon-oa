# Dijkstra from the source (and from the required vertex when one is given), then pick the cheapest favorite.
import heapq
from typing import List, Optional, Any


def _dijkstra(n: int, adj: List[List[Any]], src: int) -> List[float]:
    INF = float("inf")
    dist = [INF] * n
    if src < 0 or src >= n:
        return dist
    dist[src] = 0
    pq = [(0, src)]
    while pq:
        d, u = heapq.heappop(pq)
        if d > dist[u]:
            continue
        for v, w in adj[u]:
            nd = d + w
            if nd < dist[v]:
                dist[v] = nd
                heapq.heappush(pq, (nd, v))
    return dist


def solve(n: int, roads: List[List[int]], favorites: List[int], source: int, required: int) -> int:
    adj: List[List[Any]] = [[] for _ in range(n)]
    for road in roads:
        u, v, w = road[0], road[1], road[2]
        adj[u].append((v, w))
        adj[v].append((u, w))

    ds = _dijkstra(n, adj, source)
    INF = float("inf")

    if required is not None and 0 <= required < n:
        dr = _dijkstra(n, adj, required)

        def cost(city: int) -> float:
            if ds[required] == INF or dr[city] == INF:
                return INF
            return ds[required] + dr[city]
    else:
        def cost(city: int) -> float:
            return ds[city]

    best_city = -1
    best_cost = INF
    for city in favorites:
        if city < 0 or city >= n:
            continue
        c = cost(city)
        if c < best_cost or (c == best_cost and c != INF and city < best_city):
            best_cost = c
            best_city = city
    return best_city
