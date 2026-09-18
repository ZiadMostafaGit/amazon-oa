# Iterative subtree aggregation: count hostile nodes per subtree in reverse topological order.
from typing import List, Optional, Any


def findDefenders(names: List[str], parent: List[int], hostile: List[bool]) -> List[str]:
    n = len(names)
    children = [[] for _ in range(n)]
    roots = []
    for i in range(n):
        p = parent[i]
        if p == -1:
            roots.append(i)
        else:
            children[p].append(i)
    order = []
    stack = list(roots)
    while stack:
        node = stack.pop()
        order.append(node)
        for c in children[node]:
            stack.append(c)
    counts = [1 if hostile[i] else 0 for i in range(n)]
    for node in reversed(order):
        p = parent[node]
        if p != -1:
            counts[p] += counts[node]
    total_hostile = sum(1 for h in hostile if h)
    res = []
    for i in range(n):
        if not hostile[i] and counts[i] == total_hostile:
            res.append(names[i])
    return res
