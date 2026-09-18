# Grid bucketing with side k plus union-find: only the 9 neighbouring buckets can hold edges.
from typing import List, Optional, Any


def groupSparsePoints(points: List[List[int]], k: int) -> List[List[int]]:
    n = len(points)
    if n == 0:
        return []

    parent = list(range(n))

    def find(x: int) -> int:
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    def union(a: int, b: int) -> None:
        ra, rb = find(a), find(b)
        if ra != rb:
            if ra < rb:
                parent[rb] = ra
            else:
                parent[ra] = rb

    buckets = {}
    cells = [None] * n
    for i, (x, y) in enumerate(points):
        c = (x // k, y // k)
        cells[i] = c
        buckets.setdefault(c, []).append(i)

    limit = k * k
    for i in range(n):
        xi, yi = points[i]
        cx, cy = cells[i]
        for dx in (-1, 0, 1):
            for dy in (-1, 0, 1):
                for j in buckets.get((cx + dx, cy + dy), ()):
                    if j <= i:
                        continue
                    ddx = xi - points[j][0]
                    ddy = yi - points[j][1]
                    if ddx * ddx + ddy * ddy < limit:
                        union(i, j)

    groups = {}
    for i in range(n):
        groups.setdefault(find(i), []).append(i)
    return [groups[r] for r in sorted(groups, key=lambda r: groups[r][0])]
