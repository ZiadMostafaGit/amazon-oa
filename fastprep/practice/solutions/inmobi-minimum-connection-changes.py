# Union-Find: answer is (components - 1) if wires >= n-1, else -1.
from typing import List, Optional, Any


def minimumConnectionChanges(n: int, connections: List[List[int]]) -> int:
    if len(connections) < n - 1:
        return -1

    parent = list(range(n + 1))
    rank = [0] * (n + 1)

    def find(x: int) -> int:
        root = x
        while parent[root] != root:
            root = parent[root]
        while parent[x] != root:
            parent[x], x = root, parent[x]
        return root

    components = n
    for a, b in connections:
        ra, rb = find(a), find(b)
        if ra == rb:
            continue
        if rank[ra] < rank[rb]:
            ra, rb = rb, ra
        parent[rb] = ra
        if rank[ra] == rank[rb]:
            rank[ra] += 1
        components -= 1

    return components - 1
