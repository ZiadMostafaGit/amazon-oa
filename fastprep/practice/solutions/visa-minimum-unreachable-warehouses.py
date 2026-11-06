from typing import List, Optional, Any


def minimumUnreachableWarehouses(warehouseNodes: int, warehouseFrom: List[int], warehouseTo: List[int]) -> int:
    n = warehouseNodes
    parent = list(range(n + 1))
    size = [1] * (n + 1)
    edges = [0] * (n + 1)

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    for a, b in zip(warehouseFrom, warehouseTo):
        ra, rb = find(a), find(b)
        if ra != rb:
            if size[ra] < size[rb]:
                ra, rb = rb, ra
            parent[rb] = ra
            size[ra] += size[rb]
            edges[ra] += edges[rb]
        edges[ra] += 1
    return sum(1 for v in range(1, n + 1) if find(v) == v and edges[v] == size[v] - 1)
