# Two boundary searches: first index >= target and first index > target.
from typing import List, Optional, Any


def _first(nums: List[int], pred) -> int:
    lo, hi = 0, len(nums)
    while lo < hi:
        mid = (lo + hi) // 2
        if pred(nums[mid]):
            hi = mid
        else:
            lo = mid + 1
    return lo


def findFirstAndLastOccurrence(nums: List[int], target: int) -> List[int]:
    left = _first(nums, lambda v: v >= target)
    if left == len(nums) or nums[left] != target:
        return [-1, -1]
    right = _first(nums, lambda v: v > target) - 1
    return [left, right]
