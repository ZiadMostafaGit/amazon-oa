# Union-Find (disjoint set) with path compression, adding cells one at a time.
from typing import List, Optional, Any


def numIslands2(rows: int, cols: int, positions: List[List[int]]) -> List[int]:
    parent = {}
    rank = {}
    count = 0
    res = []

    def find(x):
        root = x
        while parent[root] != root:
            root = parent[root]
        while parent[x] != root:
            parent[x], x = root, parent[x]
        return root

    for r, c in positions:
        idx = r * cols + c
        if idx in parent:
            res.append(count)
            continue
        parent[idx] = idx
        rank[idx] = 0
        count += 1
        for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols:
                nidx = nr * cols + nc
                if nidx in parent:
                    a, b = find(idx), find(nidx)
                    if a != b:
                        if rank[a] < rank[b]:
                            a, b = b, a
                        parent[b] = a
                        if rank[a] == rank[b]:
                            rank[a] += 1
                        count -= 1
        res.append(count)
    return res
