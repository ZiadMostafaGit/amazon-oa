# Union-find with the two-parent / cycle case analysis of Redundant Connection II.
from typing import List, Optional, Any


def findRedundantDirectedConnection(edges: List[List[int]]) -> List[int]:
    n = len(edges)
    parent_edge = [-1] * (n + 1)
    cand1 = None  # first edge into the node that has two parents
    cand2 = None  # second (later) edge into that node

    for i, (u, v) in enumerate(edges):
        if parent_edge[v] != -1:
            cand1 = edges[parent_edge[v]]
            cand2 = edges[i]
        else:
            parent_edge[v] = i

    dsu = list(range(n + 1))

    def find(x):
        while dsu[x] != x:
            dsu[x] = dsu[dsu[x]]
            x = dsu[x]
        return x

    cycle_edge = None
    for e in edges:
        if cand2 is not None and e is cand2:
            continue
        ru, rv = find(e[0]), find(e[1])
        if ru == rv:
            cycle_edge = e
            break
        dsu[rv] = ru

    if cycle_edge is not None:
        return cand1 if cand1 is not None else cycle_edge
    return cand2
