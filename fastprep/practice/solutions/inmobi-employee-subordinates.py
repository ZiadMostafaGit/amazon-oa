# Build the hierarchy tree, order nodes by BFS from the root, then accumulate subtree sizes in reverse order.
from typing import List, Optional, Any


def countSubordinates(bosses: List[int]) -> List[int]:
    n = len(bosses) + 1
    children = [[] for _ in range(n + 1)]
    for i, boss in enumerate(bosses):
        children[boss].append(i + 2)

    order = []
    stack = [1]
    while stack:
        node = stack.pop()
        order.append(node)
        for child in children[node]:
            stack.append(child)

    counts = [0] * (n + 1)
    for node in reversed(order):
        total = 0
        for child in children[node]:
            total += counts[child] + 1
        counts[node] = total
    return counts[1:]
