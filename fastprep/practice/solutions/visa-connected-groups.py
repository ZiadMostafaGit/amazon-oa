# Union-find over the upper triangle of the relation matrix; count roots.
from typing import List, Optional, Any


def countConnectedGroups(related: List[List[int]]) -> int:
    n = len(related)
    parent = list(range(n))

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    groups = n
    for i in range(n):
        row = related[i]
        for j in range(i + 1, n):
            if row[j]:
                a, b = find(i), find(j)
                if a != b:
                    parent[a] = b
                    groups -= 1
    return groups
