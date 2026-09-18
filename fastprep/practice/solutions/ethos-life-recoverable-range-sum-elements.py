# Prefix-sum DSU: edge (l-1, r) per measurement; A[i] is determined iff i-1 and i share a component.
from typing import List, Optional, Any


def recoverableIndices(n: int, left: List[int], right: List[int]) -> List[int]:
    parent = list(range(n + 1))
    rank = [0] * (n + 1)

    def find(x: int) -> int:
        root = x
        while parent[root] != root:
            root = parent[root]
        while parent[x] != root:
            parent[x], x = root, parent[x]
        return root

    def union(a: int, b: int) -> None:
        ra, rb = find(a), find(b)
        if ra == rb:
            return
        if rank[ra] < rank[rb]:
            ra, rb = rb, ra
        parent[rb] = ra
        if rank[ra] == rank[rb]:
            rank[ra] += 1

    m = min(len(left), len(right))
    for j in range(m):
        l = left[j]
        r = right[j]
        if 1 <= l <= r <= n:
            union(l - 1, r)

    return [i for i in range(1, n + 1) if find(i - 1) == find(i)]
