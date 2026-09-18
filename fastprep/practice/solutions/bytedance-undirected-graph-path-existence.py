# Union-find with path compression and union by size; source and destination share a root.
from typing import List, Optional, Any


def validPath(n: int, edges: List[List[int]], source: int, destination: int) -> bool:
    parent = list(range(n))
    size = [1] * n

    def find(x):
        root = x
        while parent[root] != root:
            root = parent[root]
        while parent[x] != root:
            parent[x], x = root, parent[x]
        return root

    for u, v in edges:
        ru, rv = find(u), find(v)
        if ru != rv:
            if size[ru] < size[rv]:
                ru, rv = rv, ru
            parent[rv] = ru
            size[ru] += size[rv]
    return find(source) == find(destination)
