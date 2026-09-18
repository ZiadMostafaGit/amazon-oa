# Iterative BFS from the root to compute each node's depth; delete exactly the nodes deeper than k.
from typing import List, Optional, Any


def minimumDepthDeletions(parent: List[int], k: int) -> List[int]:
    n = len(parent) + 1
    children = [[] for _ in range(n + 1)]
    for i, p in enumerate(parent):
        children[p].append(i + 2)

    depth = [0] * (n + 1)
    depth[1] = 1
    stack = [1]
    while stack:
        node = stack.pop()
        d = depth[node] + 1
        for child in children[node]:
            depth[child] = d
            stack.append(child)

    return [node for node in range(2, n + 1) if depth[node] > k]
