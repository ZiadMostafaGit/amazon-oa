# Binary search on the rotation pivot: compare mid against the last element.
from typing import List, Optional, Any


def findMinimum(values: List[int]) -> int:
    lo, hi = 0, len(values) - 1
    while lo < hi:
        mid = (lo + hi) // 2
        if values[mid] > values[hi]:
            lo = mid + 1
        else:
            hi = mid
    return values[lo]
