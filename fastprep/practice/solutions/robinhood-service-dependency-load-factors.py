# Reachability BFS from entry, then topological propagation of load over the reachable DAG.
from typing import List, Optional, Any
from collections import deque


def serviceLoads(names: List[str], dependencies: List[List[int]], entry: int) -> List[str]:
    n = len(names)
    adj = [[] for _ in range(n)]
    for u, v in dependencies:
        adj[u].append(v)

    reachable = [False] * n
    reachable[entry] = True
    stack = [entry]
    while stack:
        u = stack.pop()
        for v in adj[u]:
            if not reachable[v]:
                reachable[v] = True
                stack.append(v)

    indeg = [0] * n
    for u in range(n):
        if not reachable[u]:
            continue
        for v in adj[u]:
            indeg[v] += 1

    load = [0] * n
    load[entry] = 1
    q = deque(u for u in range(n) if reachable[u] and indeg[u] == 0)
    while q:
        u = q.popleft()
        for v in adj[u]:
            load[v] += load[u]
            indeg[v] -= 1
            if indeg[v] == 0:
                q.append(v)

    res = [(names[u], load[u]) for u in range(n) if reachable[u]]
    res.sort()
    return ["%s %d" % (name, val) for name, val in res]
