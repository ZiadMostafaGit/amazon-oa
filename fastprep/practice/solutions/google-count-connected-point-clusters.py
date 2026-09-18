# Union-Find over all O(n^2) pairs with squared-distance comparison (no floating point).
from typing import List


def countConnectedPointClusters(points: List[List[int]], r: int) -> int:
    n = len(points)
    parent = list(range(n))

    def find(x: int) -> int:
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    rr = r * r
    comps = n
    for i in range(n):
        xi, yi = points[i]
        for j in range(i + 1, n):
            xj, yj = points[j]
            dx = xi - xj
            dy = yi - yj
            if dx * dx + dy * dy <= rr:
                a, b = find(i), find(j)
                if a != b:
                    parent[a] = b
                    comps -= 1
    return comps
