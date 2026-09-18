# Union-Find over row ids and column ids: answer is stones minus the number of components.
from typing import List, Optional, Any


def removeStones(stones: List[List[int]]) -> int:
    parent = {}

    def find(x):
        parent.setdefault(x, x)
        root = x
        while parent[root] != root:
            root = parent[root]
        while parent[x] != root:
            parent[x], x = root, parent[x]
        return root

    def union(a, b):
        ra, rb = find(a), find(b)
        if ra != rb:
            parent[ra] = rb

    for r, c in stones:
        union(('r', r), ('c', c))

    roots = {find(('r', r)) for r, c in stones}
    return len(stones) - len(roots)
