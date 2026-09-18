# Union-Find over horse-parent edges, then check whether the two horses share a component.
from typing import List, Optional, Any


def solve(horseIds: List[str], motherIds: List[str], fatherIds: List[str], horseA: str, horseB: str) -> bool:
    if horseA == horseB:
        return True
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

    n = len(horseIds)
    for i in range(n):
        h = horseIds[i]
        find(h)
        m = motherIds[i] if motherIds and i < len(motherIds) else ""
        f = fatherIds[i] if fatherIds and i < len(fatherIds) else ""
        if m:
            union(h, m)
        if f:
            union(h, f)
    if horseA not in parent or horseB not in parent:
        return False
    return find(horseA) == find(horseB)
