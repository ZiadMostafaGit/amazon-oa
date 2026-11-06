from typing import List, Optional, Any


def maximumTruckWeight(n: int, roads: List[List[int]], start: int, end: int) -> int:
    parent = list(range(n))
    rank = [0] * n

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    def union(a, b):
        ra, rb = find(a), find(b)
        if ra == rb:
            return
        if rank[ra] < rank[rb]:
            ra, rb = rb, ra
        parent[rb] = ra
        if rank[ra] == rank[rb]:
            rank[ra] += 1

    # add roads from the strongest down; the limit that first joins start and end is the answer
    for a, b, limit in sorted(roads, key=lambda r: -r[2]):
        union(a, b)
        if find(start) == find(end):
            return limit
    return -1
