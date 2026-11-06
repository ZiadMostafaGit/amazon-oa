from typing import List


def lowestCommonAncestor(children: List[List[int]], p: int, q: int) -> int:
    n = len(children)
    parent = [-1] * n
    depth = [0] * n
    stack = [0]
    while stack:
        v = stack.pop()
        for c in children[v]:
            parent[c] = v
            depth[c] = depth[v] + 1
            stack.append(c)
    # Lift the deeper node, then lift both together until they meet.
    while depth[p] > depth[q]:
        p = parent[p]
    while depth[q] > depth[p]:
        q = parent[q]
    while p != q:
        p, q = parent[p], parent[q]
    return p
