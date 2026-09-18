# Sort events by time and union-find until the component count drops to one.
from typing import List, Optional, Any


def earliestFullConnection(n: int, events: List[List[int]]) -> int:
    if n == 1:
        return 0
    parent = list(range(n))
    rank = [0] * n

    def find(x: int) -> int:
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    comps = n
    for t, u, v in sorted(events, key=lambda e: e[0]):
        ru, rv = find(u), find(v)
        if ru != rv:
            if rank[ru] < rank[rv]:
                ru, rv = rv, ru
            parent[rv] = ru
            if rank[ru] == rank[rv]:
                rank[ru] += 1
            comps -= 1
            if comps == 1:
                return t
    return -1
