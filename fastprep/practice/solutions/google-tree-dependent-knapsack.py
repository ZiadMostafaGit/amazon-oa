# Dependency knapsack on the preorder: at preorder position i, either select node i (and continue
# into its subtree at i + 1) or skip it, which forbids its whole subtree (jump to i + size).
# dp[i][c] = best value from positions i.. with budget c. O(n * capacity).
from typing import List


def maximizeDependentValue(parent: List[int], cost: List[int], value: List[int], capacity: int) -> int:
    n = len(parent)
    children = [[] for _ in range(n)]
    root = 0
    for i, p in enumerate(parent):
        if p == -1:
            root = i
        else:
            children[p].append(i)
    order, stack = [], [root]
    while stack:
        v = stack.pop()
        order.append(v)
        stack.extend(reversed(children[v]))
    size = [1] * n
    for v in reversed(order):
        for ch in children[v]:
            size[v] += size[ch]
    nxt_row = [[0] * (capacity + 1) for _ in range(n + 1)]
    NEG = float("-inf")
    for i in range(n - 1, -1, -1):
        v = order[i]
        skip = nxt_row[i + size[v]]
        take = nxt_row[i + 1]
        w, val = cost[v], value[v]
        row = list(skip)
        for c in range(w, capacity + 1):
            t = take[c - w] + val
            if t > row[c]:
                row[c] = t
        nxt_row[i] = row
    return nxt_row[0][capacity]
