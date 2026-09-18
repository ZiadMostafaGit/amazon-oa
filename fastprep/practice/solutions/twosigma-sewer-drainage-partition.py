# Subtree sums via reverse index order (parent[i] < i), then minimize |total - 2*subtree|.
from typing import List, Optional, Any


def drainagePartition(parent: List[int], input: List[int]) -> int:
    n = len(parent)
    sub = list(input)
    for i in range(n - 1, 0, -1):
        sub[parent[i]] += sub[i]
    total = sub[0]
    best = None
    for i in range(1, n):
        d = abs(total - 2 * sub[i])
        if best is None or d < best:
            best = d
    return best if best is not None else 0
