# Minimax path via Kruskal: union edges in increasing weight until source and destination connect.
from typing import List, Optional, Any


def getMinimumStress(graph_nodes: int, graph_from: List[int], graph_to: List[int], graph_weight: List[int], source: int, destination: int) -> int:
    if source == destination:
        return 0
    parent = list(range(graph_nodes + 1))
    rank = [0] * (graph_nodes + 1)

    def find(x: int) -> int:
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    def union(a: int, b: int) -> None:
        ra, rb = find(a), find(b)
        if ra == rb:
            return
        if rank[ra] < rank[rb]:
            ra, rb = rb, ra
        parent[rb] = ra
        if rank[ra] == rank[rb]:
            rank[ra] += 1

    edges = sorted(zip(graph_weight, graph_from, graph_to))
    for w, u, v in edges:
        union(u, v)
        if find(source) == find(destination):
            return w
    return -1
