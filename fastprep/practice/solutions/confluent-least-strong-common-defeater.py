# Bitset reachability over a reverse-topological order, then keep minimal qualifying nodes.
from typing import List, Optional, Any


def leastStrongDefeater(monsters: List[str], defeats: List[List[str]], targets: List[str]) -> str:
    idx = {name: i for i, name in enumerate(monsters)}
    n = len(monsters)
    adj = [set() for _ in range(n)]
    indeg = [0] * n
    for a, b in defeats:
        u, v = idx[a], idx[b]
        if v not in adj[u]:
            adj[u].add(v)
            indeg[v] += 1

    order = []
    stack = [i for i in range(n) if indeg[i] == 0]
    while stack:
        u = stack.pop()
        order.append(u)
        for v in adj[u]:
            indeg[v] -= 1
            if indeg[v] == 0:
                stack.append(v)

    reach = [0] * n
    for u in reversed(order):
        m = 0
        for v in adj[u]:
            m |= (1 << v) | reach[v]
        reach[u] = m

    target_mask = 0
    for t in targets:
        target_mask |= 1 << idx[t]

    qualifying = [u for u in range(n) if reach[u] & target_mask == target_mask]
    qmask = 0
    for u in qualifying:
        qmask |= 1 << u

    best = ""
    for u in qualifying:
        if reach[u] & qmask & ~(1 << u):
            continue
        name = monsters[u]
        if best == "" or name < best:
            best = name
    return best
