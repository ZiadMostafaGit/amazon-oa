# Maximum spanning tree (Kruskal on descending XOR edge weights) over the complete graph.
from typing import List, Optional, Any


def maximumXorScore(nums: List[int]) -> int:
    n = len(nums)
    if n <= 1:
        return 0
    edges = []
    for i in range(n):
        a = nums[i]
        for j in range(i + 1, n):
            edges.append((a ^ nums[j], i, j))
    edges.sort(reverse=True)
    parent = list(range(n))

    def find(x: int) -> int:
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    total = 0
    used = 0
    for w, i, j in edges:
        ri, rj = find(i), find(j)
        if ri != rj:
            parent[ri] = rj
            total += w
            used += 1
            if used == n - 1:
                break
    return total
