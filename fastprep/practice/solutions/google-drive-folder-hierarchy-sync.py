from typing import List, Optional, Any


def findMinIncrease(tree_nodes: int, tree_from: List[int], tree_to: List[int], access_levels: List[int]) -> int:
    # The least feasible level of v is max over u of (a[u] - dist(u, v)).
    n = tree_nodes
    adj = [[] for _ in range(n + 1)]
    for u, v in zip(tree_from, tree_to):
        adj[u].append(v)
        adj[v].append(u)
    a = [0] + list(access_levels)
    parent = [0] * (n + 1)
    order = [1]
    seen = [False] * (n + 1)
    seen[1] = True
    for u in order:
        for w in adj[u]:
            if not seen[w]:
                seen[w] = True
                parent[w] = u
                order.append(w)
    best = a[:]
    for u in reversed(order):  # pull up from children
        p = parent[u]
        if p and best[u] - 1 > best[p]:
            best[p] = best[u] - 1
    for u in order:  # push down from parent
        p = parent[u]
        if p and best[p] - 1 > best[u]:
            best[u] = best[p] - 1
    return sum(best[v] - a[v] for v in range(1, n + 1))
