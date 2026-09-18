# Bottom-up tree DP (children have larger indices): each directory picks min(one directory call, sum of children costs).
from typing import List, Optional, Any


def minimumEncryptionCost(parent: List[int], type: List[int], encrypted: List[bool], cost: List[int]) -> int:
    n = len(parent)
    child_sum = [0] * n
    has_unenc = [False] * n
    best = 0
    for i in range(n - 1, -1, -1):
        if type[i] == 1:
            h = not encrypted[i]
            d = cost[i] if h else 0
        else:
            h = has_unenc[i]
            d = min(child_sum[i], cost[i]) if h else 0
        if i == 0:
            best = d
        else:
            p = parent[i]
            child_sum[p] += d
            if h:
                has_unenc[p] = True
    return best
