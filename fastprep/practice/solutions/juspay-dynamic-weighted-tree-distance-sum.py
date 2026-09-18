# Euler-tour BIT (range-update/point-query root distances) + binary-lifting LCA.
from typing import List, Optional, Any


def sumTreeQueryDistances(n: int, edges: List[List[int]], queries: List[List[int]]) -> int:
    if n == 1:
        # Only self-distance queries are possible; every answer is 0.
        return 0

    adj_head = [-1] * (n + 1)
    nxt = [-1] * (2 * (n - 1))
    dest = [0] * (2 * (n - 1))
    wt = [0] * (2 * (n - 1))
    idx = 0
    for u, v, w in edges:
        dest[idx] = v
        wt[idx] = w
        nxt[idx] = adj_head[u]
        adj_head[u] = idx
        idx += 1
        dest[idx] = u
        wt[idx] = w
        nxt[idx] = adj_head[v]
        adj_head[v] = idx
        idx += 1

    LOG = max(1, (n).bit_length())
    parent = [0] * (n + 1)
    depth = [0] * (n + 1)
    base = [0] * (n + 1)  # initial root distance
    tin = [0] * (n + 1)
    tout = [0] * (n + 1)
    order = []

    timer = 0
    parent[1] = 0
    visited = [False] * (n + 1)
    visited[1] = True
    stack = [(1, adj_head[1])]
    tin[1] = timer
    timer += 1
    order.append(1)
    while stack:
        u, e = stack.pop()
        advanced = False
        while e != -1:
            v = dest[e]
            w = wt[e]
            e2 = nxt[e]
            if not visited[v]:
                visited[v] = True
                parent[v] = u
                depth[v] = depth[u] + 1
                base[v] = base[u] + w
                tin[v] = timer
                timer += 1
                order.append(v)
                stack.append((u, e2))
                stack.append((v, adj_head[v]))
                advanced = True
                break
            e = e2
        if not advanced:
            tout[u] = timer - 1

    # tout fix: compute via reverse order of Euler entry times
    tout = [0] * (n + 1)
    for v in reversed(order):
        if tout[v] == 0:
            tout[v] = tin[v]
        p = parent[v]
        if p and tout[p] < tout[v]:
            tout[p] = tout[v]

    # binary lifting
    up = [[0] * (n + 1) for _ in range(LOG)]
    up[0] = parent[:]
    for k in range(1, LOG):
        prev = up[k - 1]
        cur = up[k]
        for v in range(1, n + 1):
            cur[v] = prev[prev[v]]

    size = n + 1
    tree = [0] * (size + 1)

    def bit_add(i: int, val: int) -> None:
        i += 1
        while i <= size:
            tree[i] += val
            i += i & (-i)

    def bit_query(i: int) -> int:
        i += 1
        s = 0
        while i > 0:
            s += tree[i]
            i -= i & (-i)
        return s

    def lca(a: int, b: int) -> int:
        if depth[a] < depth[b]:
            a, b = b, a
        diff = depth[a] - depth[b]
        k = 0
        while diff:
            if diff & 1:
                a = up[k][a]
            diff >>= 1
            k += 1
        if a == b:
            return a
        for k in range(LOG - 1, -1, -1):
            if up[k][a] != up[k][b]:
                a = up[k][a]
                b = up[k][b]
        return parent[a]

    edge_child = {}
    cur_w = {}
    for u, v, w in edges:
        c = v if parent[v] == u else u
        key = (u, v) if u < v else (v, u)
        edge_child[key] = c
        cur_w[key] = w

    total = 0
    for q in queries:
        if q[0] == 1:
            _, u, v, nw = q
            key = (u, v) if u < v else (v, u)
            delta = nw - cur_w[key]
            if delta:
                cur_w[key] = nw
                c = edge_child[key]
                bit_add(tin[c], delta)
                bit_add(tout[c] + 1, -delta)
        else:
            _, u, v = q
            if u == v:
                continue
            l = lca(u, v)
            du = base[u] + bit_query(tin[u])
            dv = base[v] + bit_query(tin[v])
            dl = base[l] + bit_query(tin[l])
            total += du + dv - 2 * dl
    return total
