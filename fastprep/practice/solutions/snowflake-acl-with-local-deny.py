# Topological propagation of allow sets over the DAG, with deny applied only locally at query time.
from typing import List, Optional, Any
from collections import deque


def canAccess(allows: List[str], denies: List[str], edges: List[List[int]], queryNodes: List[int], permissions: str) -> List[bool]:
    n = len(allows)
    children = [[] for _ in range(n)]
    indeg = [0] * n
    for p, c in edges:
        children[p].append(c)
        indeg[c] += 1

    # allowed[v] = bitmask of permissions allowed at v or at any ancestor of v
    allowed = [0] * n
    for v in range(n):
        m = 0
        for ch in allows[v]:
            m |= 1 << (ord(ch) - 97)
        allowed[v] = m

    q = deque(v for v in range(n) if indeg[v] == 0)
    order = []
    while q:
        v = q.popleft()
        order.append(v)
        for c in children[v]:
            indeg[c] -= 1
            if indeg[c] == 0:
                q.append(c)
    # propagate along topological order; deny never blocks propagation
    for v in order:
        av = allowed[v]
        for c in children[v]:
            allowed[c] |= av

    denied = [0] * n
    for v in range(n):
        m = 0
        for ch in denies[v]:
            m |= 1 << (ord(ch) - 97)
        denied[v] = m

    res = []
    for i, node in enumerate(queryNodes):
        bit = 1 << (ord(permissions[i]) - 97)
        res.append(bool(allowed[node] & bit) and not (denied[node] & bit))
    return res
