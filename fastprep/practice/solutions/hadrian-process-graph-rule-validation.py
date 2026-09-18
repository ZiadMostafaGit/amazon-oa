# Three topological-order DAG scans: C-free reach to D, B-free source-to-sink path, and A reaching a later B.
from typing import List
from collections import deque


def isValidProcessSystem(processTypes: str, edges: List[List[int]]) -> bool:
    n = len(processTypes)
    adj = [[] for _ in range(n)]
    rev = [[] for _ in range(n)]
    indeg = [0] * n
    outdeg = [0] * n
    for u, v in edges:
        adj[u].append(v)
        rev[v].append(u)
        indeg[v] += 1
        outdeg[u] += 1

    order = []
    dq = deque(i for i in range(n) if indeg[i] == 0)
    deg = indeg[:]
    while dq:
        u = dq.popleft()
        order.append(u)
        for v in adj[u]:
            deg[v] -= 1
            if deg[v] == 0:
                dq.append(v)
    if len(order) < n:
        return False

    t = processTypes
    # Rule 3: a D reachable from a source with no C strictly before it.
    clean = [False] * n
    for u in order:
        if indeg[u] == 0:
            clean[u] = True
        else:
            ok = False
            for p in rev[u]:
                if clean[p] and t[p] != 'C':
                    ok = True
                    break
            clean[u] = ok
        if clean[u] and t[u] == 'D':
            return False

    # Rule 1: a complete path with no B at all.
    nob = [False] * n
    for u in order:
        if t[u] == 'B':
            nob[u] = False
            continue
        if indeg[u] == 0:
            nob[u] = True
        else:
            nob[u] = any(nob[p] for p in rev[u])
        if nob[u] and outdeg[u] == 0:
            return False

    # Rule 2: an A that can reach a strictly later B.
    reach_b = [False] * n
    for u in reversed(order):
        r = (t[u] == 'B')
        if not r:
            for v in adj[u]:
                if reach_b[v]:
                    r = True
                    break
        reach_b[u] = r
        if t[u] == 'A':
            for v in adj[u]:
                if reach_b[v]:
                    return False
    return True
