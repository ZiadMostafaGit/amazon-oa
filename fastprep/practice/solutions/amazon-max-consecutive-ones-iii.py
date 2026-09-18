# Sliding window keeping at most k zeros inside the window.
from typing import List, Optional, Any


def solve(nums: List[int], k: int) -> int:
    left = 0
    zeros = 0
    best = 0
    for right, v in enumerate(nums):
        if v == 0:
            zeros += 1
        while zeros > k:
            if nums[left] == 0:
                zeros -= 1
            left += 1
        best = max(best, right - left + 1)
    return best
