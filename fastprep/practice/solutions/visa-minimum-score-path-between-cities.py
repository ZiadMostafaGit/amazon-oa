from typing import List


def minScore(n: int, roads: List[List[int]]) -> int:
    parent = list(range(n + 1))

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    for a, b, _ in roads:
        ra, rb = find(a), find(b)
        if ra != rb:
            parent[ra] = rb
    root = find(1)
    return min(d for a, _, d in roads if find(a) == root)
