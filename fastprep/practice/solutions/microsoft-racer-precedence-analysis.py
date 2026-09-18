# Kahn topological sort: cycle if not all nodes emitted, unique order if each step had one choice.
from typing import List, Optional, Any
from collections import deque


def analyzeRaceOrder(relations: List[List[str]]) -> List[str]:
    adj = {}
    indeg = {}
    seen_edges = set()

    def node(name: str):
        if name not in adj:
            adj[name] = set()
            indeg[name] = 0

    for rel in relations:
        before, after = rel[0], rel[1]
        node(before)
        node(after)
        key = (before, after)
        if key in seen_edges:
            continue
        seen_edges.add(key)
        adj[before].add(after)
        indeg[after] += 1

    q = deque(sorted(n for n in adj if indeg[n] == 0))
    unique = True
    order = []
    while q:
        if len(q) > 1:
            unique = False
        cur = q.popleft()
        order.append(cur)
        for nxt in adj[cur]:
            indeg[nxt] -= 1
            if indeg[nxt] == 0:
                q.append(nxt)

    acyclic = len(order) == len(adj)
    if not acyclic:
        return ["false", "false", "", ""]
    if not unique:
        return ["true", "false", "", ""]
    if not order:
        return ["true", "true", "", ""]
    return ["true", "true", order[0], order[-1]]
