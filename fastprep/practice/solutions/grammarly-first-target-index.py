# Lower bound: the first index with nums[i] >= target, then check it is the target.
from typing import List, Optional, Any


def firstTargetIndex(nums: List[int], target: int) -> int:
    lo, hi = 0, len(nums)
    while lo < hi:
        mid = (lo + hi) // 2
        if nums[mid] >= target:
            hi = mid
        else:
            lo = mid + 1
    return lo if lo < len(nums) and nums[lo] == target else -1
