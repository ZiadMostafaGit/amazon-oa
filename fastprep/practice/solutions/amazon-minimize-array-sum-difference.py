# Drop indices whose neighbouring differences telescope, greedily left to right
# and never two in a row, so every removal provably keeps the total cost.
from typing import List, Optional, Any


def minimizeArraySumDifference(arr: List[int]) -> List[int]:
    n = len(arr)
    if n <= 2:
        return list(arr)
    drop = [False] * n
    i = 1
    while i < n - 1:
        left = arr[i - 1]
        mid = arr[i]
        right = arr[i + 1]
        if abs(left - mid) + abs(mid - right) == abs(left - right):
            drop[i] = True
            i += 2          # keep the next element so removals stay independent
        else:
            i += 1
    return [v for j, v in enumerate(arr) if not drop[j]]
