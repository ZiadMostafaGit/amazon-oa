# DAG path counting: routes through edge (u,v) = paths(0->u) * paths(v->n-1); pick max via topological order.
from typing import List


def bestRoadToIncrease(n: int, roads: List[List[int]]) -> int:
    adj = [[] for _ in range(n)]
    radj = [[] for _ in range(n)]
    indeg = [0] * n
    for u, v, _t in roads:
        adj[u].append(v)
        radj[v].append(u)
        indeg[v] += 1

    # Kahn topological order
    order = []
    stack = [i for i in range(n) if indeg[i] == 0]
    while stack:
        u = stack.pop()
        order.append(u)
        for v in adj[u]:
            indeg[v] -= 1
            if indeg[v] == 0:
                stack.append(v)

    src = 0
    dst = n - 1
    f = [0] * n  # paths from 0 to u
    f[src] = 1
    for u in order:
        if f[u]:
            fu = f[u]
            for v in adj[u]:
                f[v] += fu

    g = [0] * n  # paths from v to n-1
    g[dst] = 1
    for u in reversed(order):
        s = 0
        for v in adj[u]:
            s += g[v]
        if u != dst:
            g[u] = s
        else:
            g[u] = 1

    if f[dst] == 0:
        return -1

    best_idx = -1
    best_cnt = -1
    for i, (u, v, _t) in enumerate(roads):
        cnt = f[u] * g[v]
        if cnt > best_cnt:
            best_cnt = cnt
            best_idx = i
    return best_idx
