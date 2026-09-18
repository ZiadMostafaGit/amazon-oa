# Binary search over the left boundary of the length-k window, preferring smaller values on ties.
from typing import List, Optional, Any


def solve(arr: List[int], k: int, x: int) -> List[int]:
    n = len(arr)
    if k <= 0:
        return []
    if k >= n:
        return list(arr)
    lo, hi = 0, n - k
    while lo < hi:
        mid = (lo + hi) // 2
        # compare distance of the element leaving vs the element entering
        if x - arr[mid] > arr[mid + k] - x:
            lo = mid + 1
        else:
            hi = mid
    return list(arr[lo:lo + k])
