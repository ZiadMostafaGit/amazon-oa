# Euler-tour/tin ordering + binary-lifting LCA: LCA of a set = LCA(min-tin node, max-tin node).
from typing import List, Optional, Any


def lowestCommonManagers(employeeIds: List[int], managerIds: List[int], queries: List[List[int]]) -> List[int]:
    n = len(employeeIds)
    idx = {}
    for i, e in enumerate(employeeIds):
        idx[e] = i

    parent = [-1] * n
    children = [[] for _ in range(n)]
    root = 0
    for i in range(n):
        m = managerIds[i]
        if m == -1:
            parent[i] = -1
            root = i
        else:
            p = idx[m]
            parent[i] = p
            children[p].append(i)

    # iterative DFS for tin and depth
    tin = [0] * n
    depth = [0] * n
    timer = 0
    stack = [root]
    depth[root] = 0
    visited = [False] * n
    while stack:
        u = stack.pop()
        if visited[u]:
            continue
        visited[u] = True
        tin[u] = timer
        timer += 1
        for c in children[u]:
            depth[c] = depth[u] + 1
            stack.append(c)

    LOG = max(1, n.bit_length())
    up = [[0] * n for _ in range(LOG)]
    up[0] = [parent[i] if parent[i] != -1 else i for i in range(n)]
    for k in range(1, LOG):
        prev = up[k - 1]
        cur = up[k]
        for v in range(n):
            cur[v] = prev[prev[v]]

    def lca(u: int, v: int) -> int:
        if depth[u] < depth[v]:
            u, v = v, u
        diff = depth[u] - depth[v]
        k = 0
        while diff:
            if diff & 1:
                u = up[k][u]
            diff >>= 1
            k += 1
        if u == v:
            return u
        for k in range(LOG - 1, -1, -1):
            if up[k][u] != up[k][v]:
                u = up[k][u]
                v = up[k][v]
        return up[0][u]

    out = []
    for q in queries:
        best_lo = best_hi = idx[q[0]]
        lo_t = hi_t = tin[best_lo]
        for e in q[1:]:
            i = idx[e]
            t = tin[i]
            if t < lo_t:
                lo_t = t
                best_lo = i
            if t > hi_t:
                hi_t = t
                best_hi = i
        out.append(employeeIds[lca(best_lo, best_hi)])
    return out
