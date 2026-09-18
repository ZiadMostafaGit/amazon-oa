# Iterative DFS preorder (Euler tour) + subtree sizes; each query is an O(1) index lookup.
from typing import List, Optional, Any


def chainOfCommand(parent: List[int], queries: List[List[int]]) -> List[int]:
    n = len(parent)
    children: List[List[int]] = [[] for _ in range(n + 1)]
    root = 1
    for i in range(n):
        node = i + 1
        p = parent[i]
        if p is None or p == -1:
            root = node
        else:
            children[p].append(node)
    for c in children:
        c.sort()

    order: List[int] = []
    pos = [0] * (n + 1)      # index of node in preorder
    size = [1] * (n + 1)     # subtree size

    stack = [root]
    while stack:
        node = stack.pop()
        pos[node] = len(order)
        order.append(node)
        for ch in reversed(children[node]):
            stack.append(ch)

    # subtree sizes: process preorder in reverse, adding into parent
    for idx in range(len(order) - 1, 0, -1):
        node = order[idx]
        p = parent[node - 1]
        if p is not None and p != -1:
            size[p] += size[node]

    res: List[int] = []
    for q in queries:
        start, k = q[0], q[1]
        if k < 1 or k > size[start]:
            res.append(-1)
        else:
            res.append(order[pos[start] + k - 1])
    return res
