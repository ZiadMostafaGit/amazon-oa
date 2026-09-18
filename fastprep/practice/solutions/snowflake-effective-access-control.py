# Topological propagation of inherited allow/deny bitsets down the DAG, then allow minus deny.
from typing import List, Optional, Any
from collections import deque


def getEffectiveAccess(allowLists: List[List[str]], denyLists: List[List[str]], edges: List[List[int]]) -> List[List[str]]:
    n = len(allowLists)
    names: List[str] = []
    index = {}

    def idx(name: str) -> int:
        i = index.get(name)
        if i is None:
            i = len(names)
            index[name] = i
            names.append(name)
        return i

    allow = [0] * n
    deny = [0] * n
    for i in range(n):
        m = 0
        for name in allowLists[i]:
            m |= 1 << idx(name)
        allow[i] = m
        m = 0
        for name in denyLists[i]:
            m |= 1 << idx(name)
        deny[i] = m

    adj = [[] for _ in range(n)]
    indeg = [0] * n
    for parent, child in edges:
        adj[parent].append(child)
        indeg[child] += 1

    queue = deque(i for i in range(n) if indeg[i] == 0)
    order = []
    while queue:
        u = queue.popleft()
        order.append(u)
        for v in adj[u]:
            indeg[v] -= 1
            if indeg[v] == 0:
                queue.append(v)

    for u in order:
        au = allow[u]
        du = deny[u]
        for v in adj[u]:
            allow[v] |= au
            deny[v] |= du

    result: List[List[str]] = []
    for i in range(n):
        mask = allow[i] & ~deny[i]
        out = []
        while mask:
            low = mask & -mask
            out.append(names[low.bit_length() - 1])
            mask ^= low
        out.sort()
        result.append(out)
    return result
