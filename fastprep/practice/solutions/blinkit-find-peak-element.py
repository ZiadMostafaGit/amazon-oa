# Binary search on the slope: move toward the larger neighbour, which always contains a peak.
from typing import List, Optional, Any


def findPeakElement(nums: List[int]) -> int:
    lo, hi = 0, len(nums) - 1
    while lo < hi:
        mid = (lo + hi) // 2
        if nums[mid] < nums[mid + 1]:
            lo = mid + 1
        else:
            hi = mid
    return lo
