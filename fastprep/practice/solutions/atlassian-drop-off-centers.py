# Multi-source bounded Dijkstra per company (with Voronoi-edge trick for intra-company
# pairs) to build a company compatibility matrix, then brute-force the <=2^10 subsets.
import heapq
from typing import List, Optional, Any


def findCount(n: int, graphFrom: List[int], graphTo: List[int], graphWeight: List[int], minDistance: int, company: List[int]) -> int:
    INF = float('inf')
    adj: List[List[Any]] = [[] for _ in range(n + 1)]
    edges = []
    for a, b, w in zip(graphFrom, graphTo, graphWeight):
        adj[a].append((b, w))
        adj[b].append((a, w))
        edges.append((a, b, w))

    # group nodes by company id
    groups = {}
    for i in range(n):
        groups.setdefault(company[i], []).append(i + 1)
    ids = sorted(groups)
    k = len(ids)

    def multi_dijkstra(sources):
        dist = [INF] * (n + 1)
        src = [0] * (n + 1)
        heap = []
        for s in sources:
            dist[s] = 0
            src[s] = s
            heap.append((0, s))
        heapq.heapify(heap)
        while heap:
            d, u = heapq.heappop(heap)
            if d > dist[u]:
                continue
            if d >= minDistance:
                break
            for v, w in adj[u]:
                nd = d + w
                if nd < dist[v]:
                    dist[v] = nd
                    src[v] = src[u]
                    heapq.heappush(heap, (nd, v))
        return dist, src

    dist_of = {}
    self_ok = {}
    for cid in ids:
        nodes = groups[cid]
        dist, src = multi_dijkstra(nodes)
        dist_of[cid] = dist
        best = INF
        if len(nodes) > 1:
            for a, b, w in edges:
                if src[a] and src[b] and src[a] != src[b]:
                    cand = dist[a] + w + dist[b]
                    if cand < best:
                        best = cand
        self_ok[cid] = best >= minDistance

    compat = [[True] * k for _ in range(k)]
    for i, cid in enumerate(ids):
        dist = dist_of[cid]
        for j, other in enumerate(ids):
            if i == j:
                continue
            if any(dist[v] < minDistance for v in groups[other]):
                compat[i][j] = False
                compat[j][i] = False

    valid = [self_ok[cid] for cid in ids]
    count = 0
    for mask in range(1, 1 << k):
        members = [i for i in range(k) if mask >> i & 1]
        if not all(valid[i] for i in members):
            continue
        good = True
        for x in range(len(members)):
            for y in range(x + 1, len(members)):
                if not compat[members[x]][members[y]]:
                    good = False
                    break
            if not good:
                break
        if good:
            count += 1
    return count
