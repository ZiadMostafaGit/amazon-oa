from typing import List, Optional, Any


def solution(A: List[int], B: List[int], S: int) -> bool:
    parent = list(range(S + 1))
    nodes = [1] * (S + 1)
    edges = [0] * (S + 1)

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    for a, b in zip(A, B):
        ra, rb = find(a), find(b)
        if ra != rb:
            parent[ra] = rb
            nodes[rb] += nodes[ra]
            edges[rb] += edges[ra]
            ra = rb
        edges[ra] += 1
        if edges[ra] > nodes[ra]:
            return False
    return True
