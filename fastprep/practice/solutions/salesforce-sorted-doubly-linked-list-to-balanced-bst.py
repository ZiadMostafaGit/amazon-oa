# Recursive divide and conquer over index ranges, lower-middle as root, emitting a link table.
from typing import List, Optional, Any


def buildBalancedBstLinks(values: List[int]) -> List[List[int]]:
    n = len(values)
    left = [-1] * n
    right = [-1] * n
    parent = [-1] * n

    # iterative stack of (lo, hi, parent) over half-open ranges
    stack = [(0, n, -1, 0)]  # last field: 0 = left child of parent, 1 = right, 2 = root
    while stack:
        lo, hi, par, side = stack.pop()
        if lo >= hi:
            continue
        mid = lo + (hi - lo - 1) // 2
        parent[mid] = par
        if side == 0 and par != -1:
            left[par] = mid
        elif side == 1 and par != -1:
            right[par] = mid
        stack.append((lo, mid, mid, 0))
        stack.append((mid + 1, hi, mid, 1))

    return [[i, left[i], right[i], parent[i]] for i in range(n)]
