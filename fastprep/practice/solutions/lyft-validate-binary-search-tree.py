# Iterative DFS carrying (low, high) bounds down each branch.
from typing import List, Optional, Any


def isValidBST(values: List[int], left: List[int], right: List[int], root: int) -> bool:
    if root is None or root == -1 or not values:
        return True
    stack = [(root, None, None)]
    while stack:
        idx, low, high = stack.pop()
        v = values[idx]
        if low is not None and v <= low:
            return False
        if high is not None and v >= high:
            return False
        li = left[idx]
        ri = right[idx]
        if li != -1:
            stack.append((li, low, v))
        if ri != -1:
            stack.append((ri, v, high))
    return True
