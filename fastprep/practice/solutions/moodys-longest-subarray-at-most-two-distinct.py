# Sliding window keeping a count map of at most two distinct values.
from typing import List, Optional, Any


def longestSubarrayAtMostTwoDistinct(nums: List[int]) -> int:
    counts = {}
    left = 0
    best = 0
    for right, v in enumerate(nums):
        counts[v] = counts.get(v, 0) + 1
        while len(counts) > 2:
            lv = nums[left]
            counts[lv] -= 1
            if counts[lv] == 0:
                del counts[lv]
            left += 1
        if right - left + 1 > best:
            best = right - left + 1
    return best
