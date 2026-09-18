# Iterative post-order subtree sizes, then count nodes whose child sizes are all equal.
from typing import List, Optional, Any


def solution(subtrees: List[List[int]]) -> int:
    n = len(subtrees)
    if n == 0:
        return 0
    size = [1] * n
    order = []
    stack = [0]
    while stack:
        node = stack.pop()
        order.append(node)
        for child in subtrees[node]:
            stack.append(child)
    for node in reversed(order):
        total = 1
        for child in subtrees[node]:
            total += size[child]
        size[node] = total
    count = 0
    for node in range(n):
        kids = subtrees[node]
        if len(kids) <= 1:
            count += 1
            continue
        first = size[kids[0]]
        if all(size[c] == first for c in kids):
            count += 1
    return count
