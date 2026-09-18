# Binary search on the offset nums[i] - nums[0] - i to find the first index past a gap.
from typing import List, Optional, Any


def firstMissingNumber(nums: List[int]) -> int:
    base = nums[0]
    lo, hi = 0, len(nums) - 1
    # invariant: nums[lo] - base == lo (no gap before lo), nums[hi] - base > hi
    while hi - lo > 1:
        mid = (lo + hi) // 2
        if nums[mid] - base == mid:
            lo = mid
        else:
            hi = mid
    return nums[lo] + 1
