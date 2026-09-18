# Union-Find (disjoint set union) over the adjacency matrix; count distinct roots.
from typing import List, Optional, Any


def findCircleNum(isConnected: List[List[int]]) -> int:
    n = len(isConnected)
    parent = list(range(n))

    def find(x: int) -> int:
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    def union(a: int, b: int) -> None:
        ra, rb = find(a), find(b)
        if ra != rb:
            parent[rb] = ra

    for i in range(n):
        row = isConnected[i]
        for j in range(i + 1, n):
            if row[j]:
                union(i, j)

    return sum(1 for i in range(n) if find(i) == i)
