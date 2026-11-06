from typing import List


def kthSubtreeNodes(parents: List[int], queries: List[List[int]]) -> List[int]:
    n = len(parents)
    children = [[] for _ in range(n + 1)]
    for v in range(2, n + 1):  # ascending v keeps each child list sorted
        children[parents[v - 1]].append(v)
    order = []
    tin = [0] * (n + 1)
    size = [1] * (n + 1)
    stack = [1]
    while stack:
        v = stack.pop()
        tin[v] = len(order)
        order.append(v)
        for c in reversed(children[v]):
            stack.append(c)
    for i in range(n - 1, -1, -1):
        v = order[i]
        if v != 1:
            size[parents[v - 1]] += size[v]
    out = []
    for u, k in queries:
        out.append(order[tin[u] + k - 1] if k <= size[u] else -1)
    return out
