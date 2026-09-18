# Union-Find: for each divisor d > t, union all multiples of d (harmonic total work).
from typing import List, Optional, Any


def analyzeDivisorComponents(n: int, t: int) -> List[int]:
    parent = list(range(n + 1))
    size = [1] * (n + 1)

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    def union(a, b):
        ra, rb = find(a), find(b)
        if ra == rb:
            return
        if size[ra] < size[rb]:
            ra, rb = rb, ra
        parent[rb] = ra
        size[ra] += size[rb]

    for d in range(t + 1, n + 1):
        if d == 0:
            continue
        for m in range(2 * d, n + 1, d):
            union(d, m)

    comps = 0
    best = 0
    for i in range(1, n + 1):
        if find(i) == i:
            comps += 1
            if size[i] > best:
                best = size[i]
    return [comps, best]
