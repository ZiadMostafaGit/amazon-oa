from typing import List, Optional, Any


def minCostToConnectServers(x: List[int], y: List[int]) -> int:
    n = len(x)
    # Only neighbours in x-order and in y-order can be MST edges: 2(n-1) candidates.
    edges = []
    for coord in (x, y):
        order = sorted(range(n), key=lambda i: coord[i])
        for a, b in zip(order, order[1:]):
            edges.append((coord[b] - coord[a], a, b))
    edges.sort()
    parent = list(range(n))
    size = [1] * n

    def find(v):
        while parent[v] != v:
            parent[v] = parent[parent[v]]
            v = parent[v]
        return v

    total, joined = 0, 0
    for w, a, b in edges:
        ra, rb = find(a), find(b)
        if ra == rb:
            continue
        if size[ra] < size[rb]:
            ra, rb = rb, ra
        parent[rb] = ra
        size[ra] += size[rb]
        total += w
        joined += 1
        if joined == n - 1:
            break
    return total
