from typing import List, Optional, Any


def getMinEuclideanTime(n: int, d: int, x: List[int], y: List[int]) -> int:
    parent = list(range(n))

    def find(a):
        while parent[a] != a:
            parent[a] = parent[parent[a]]
            a = parent[a]
        return a

    comps = n
    dd = d * d
    for i in range(n):
        xi, yi = x[i], y[i]
        for j in range(i + 1, n):
            dx = xi - x[j]
            dy = yi - y[j]
            if dx * dx + dy * dy <= dd:
                a, b = find(i), find(j)
                if a != b:
                    parent[a] = b
                    comps -= 1
    return comps
