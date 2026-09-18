# Union-Find over parent/child pairs, then pick the root of the component with the most nodes.
from typing import List, Optional, Any


def findLargestTreeRoot(parents: List[int], children: List[int]) -> int:
    par = {}

    def find(x: int) -> int:
        root = x
        while par[root] != root:
            root = par[root]
        while par[x] != root:
            par[x], x = root, par[x]
        return root

    has_parent = set()
    for p, c in zip(parents, children):
        par.setdefault(p, p)
        par.setdefault(c, c)
        has_parent.add(c)

    for p, c in zip(parents, children):
        rp, rc = find(p), find(c)
        if rp != rc:
            par[rp] = rc

    size = {}
    for node in par:
        r = find(node)
        size[r] = size.get(r, 0) + 1

    best_comp = None
    best_size = -1
    for r, s in size.items():
        if s > best_size:
            best_size = s
            best_comp = r

    for node in par:
        if node not in has_parent and find(node) == best_comp:
            return node
    return best_comp
