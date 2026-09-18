# Dijkstra over states (city, cheapest fuel price seen so far); an unlimited tank means
# each edge is paid at the minimum price among cities already visited on the path.
import heapq
from typing import List


def minFuelCost(n: int, roads: List[List[int]], fuelPrices: List[int], start: int, destination: int) -> int:
    if start == destination:
        return 0
    adj = [[] for _ in range(n)]
    for u, v, d in roads:
        adj[u].append((v, d))
        adj[v].append((u, d))

    prices = sorted(set(fuelPrices))
    pidx = {p: i for i, p in enumerate(prices)}
    m = len(prices)
    INF = float('inf')
    dist = [[INF] * m for _ in range(n)]

    s0 = pidx[fuelPrices[start]]
    dist[start][s0] = 0
    pq = [(0, start, s0)]
    while pq:
        cost, u, pi = heapq.heappop(pq)
        if cost > dist[u][pi]:
            continue
        if u == destination:
            return cost
        price = prices[pi]
        for v, d in adj[u]:
            vi = pidx[fuelPrices[v]]
            npi = vi if vi < pi else pi
            nc = cost + d * price
            if nc < dist[v][npi]:
                dist[v][npi] = nc
                heapq.heappush(pq, (nc, v, npi))
    return -1
