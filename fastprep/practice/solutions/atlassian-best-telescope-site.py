# Floyd-Warshall all-pairs shortest paths, then pick the city with the fewest reachable neighbors, breaking ties by the highest number.
from typing import List


def bestTelescopeSite(cityNodes: int, cityFrom: List[int], cityTo: List[int], cityWeight: List[int], distanceThreshold: int) -> int:
    INF = float('inf')
    n = cityNodes
    dist = [[INF] * n for _ in range(n)]
    for i in range(n):
        dist[i][i] = 0
    for u, v, w in zip(cityFrom, cityTo, cityWeight):
        a, b = u - 1, v - 1
        if a == b:
            continue
        if w < dist[a][b]:
            dist[a][b] = w
            dist[b][a] = w
    for k in range(n):
        dk = dist[k]
        for i in range(n):
            dik = dist[i][k]
            if dik == INF:
                continue
            di = dist[i]
            for j in range(n):
                nd = dik + dk[j]
                if nd < di[j]:
                    di[j] = nd
    best_city = -1
    best_count = None
    for i in range(n):
        cnt = 0
        for j in range(n):
            if j != i and dist[i][j] <= distanceThreshold:
                cnt += 1
        if best_count is None or cnt < best_count or (cnt == best_count and i + 1 > best_city):
            best_count = cnt
            best_city = i + 1
    return best_city
