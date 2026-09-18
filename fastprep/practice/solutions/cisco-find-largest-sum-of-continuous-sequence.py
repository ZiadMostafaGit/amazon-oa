# Kadane's algorithm for maximum contiguous subarray sum.
from typing import List, Optional, Any


def maxSubArraySum(nums: List[int]) -> int:
    if not nums:
        return 0
    best = cur = nums[0]
    for x in nums[1:]:
        cur = x if cur < 0 else cur + x
        if cur > best:
            best = cur
    return best
