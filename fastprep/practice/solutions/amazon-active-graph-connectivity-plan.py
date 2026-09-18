# Union-find/BFS: find the component reachable from start, then link each other component to it.
from typing import List, Optional, Any
from collections import deque


def solve(n: int, edges: List[List[int]], start: int) -> List[List[int]]:
    adj = [[] for _ in range(n)]
    for e in edges:
        u, v = e[0], e[1]
        adj[u].append(v)
        adj[v].append(u)

    comp = [-1] * n
    comps = []
    for s in range(n):
        if comp[s] != -1:
            continue
        cid = len(comps)
        members = []
        comp[s] = cid
        dq = deque([s])
        while dq:
            u = dq.popleft()
            members.append(u)
            for w in adj[u]:
                if comp[w] == -1:
                    comp[w] = cid
                    dq.append(w)
        members.sort()
        comps.append(members)

    active_id = comp[start]
    active = comps[active_id]
    root = active[0]

    result = [active]
    others = sorted((c[0] for i, c in enumerate(comps) if i != active_id))
    for m in others:
        result.append([root, m])
    return result
