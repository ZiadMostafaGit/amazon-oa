# Kadane's algorithm over a non-empty array.
from typing import List, Optional, Any


def maxSubarraySum(nums: List[int]) -> int:
    best = cur = nums[0]
    for x in nums[1:]:
        cur = x if cur < 0 else cur + x
        if cur > best:
            best = cur
    return best
