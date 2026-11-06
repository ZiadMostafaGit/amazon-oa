# Union-find over the upper triangle of the adjacency matrix; count roots.
from typing import List, Optional, Any


def findCircleNum(isConnected: List[List[int]]) -> int:
    n = len(isConnected)
    parent = list(range(n))

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    groups = n
    for i in range(n):
        row = isConnected[i]
        for j in range(i + 1, n):
            if row[j]:
                a, b = find(i), find(j)
                if a != b:
                    parent[a] = b
                    groups -= 1
    return groups
