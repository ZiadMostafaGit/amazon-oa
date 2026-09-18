# Union-find over nodes 1..n, then sum ceil(sqrt(size)) for each component root.
from typing import List, Optional, Any
import math


def connectedSum(n: int, graphFrom: List[int], graphTo: List[int]) -> int:
    parent = list(range(n + 1))
    size = [1] * (n + 1)

    def find(x: int) -> int:
        root = x
        while parent[root] != root:
            root = parent[root]
        while parent[x] != root:
            parent[x], x = root, parent[x]
        return root

    for a, b in zip(graphFrom, graphTo):
        ra, rb = find(a), find(b)
        if ra != rb:
            if size[ra] < size[rb]:
                ra, rb = rb, ra
            parent[rb] = ra
            size[ra] += size[rb]

    total = 0
    for node in range(1, n + 1):
        if find(node) == node:
            total += math.isqrt(size[node] - 1) + 1 if size[node] > 0 else 0
    return total
