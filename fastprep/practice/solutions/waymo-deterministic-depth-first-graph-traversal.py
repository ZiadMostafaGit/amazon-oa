# Iterative DFS with an explicit stack; neighbors sorted ascending and pushed in reverse for preorder.
from typing import List, Optional, Any


def dfsTraversal(adjacency: List[List[int]], start: int) -> List[int]:
    n = len(adjacency)
    if n == 0 or start < 0 or start >= n:
        return []
    visited = [False] * n
    order = []
    stack = [start]
    while stack:
        v = stack.pop()
        if visited[v]:
            continue
        visited[v] = True
        order.append(v)
        for nb in sorted(adjacency[v], reverse=True):
            if not visited[nb]:
                stack.append(nb)
    return order
