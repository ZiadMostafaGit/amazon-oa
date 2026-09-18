# Sort + sliding window: keep window whose cost to raise all to the window max is <= k.
from typing import List


def maxFrequency(nums: List[int], k: int) -> int:
    nums = sorted(nums)
    best = 1
    left = 0
    total = 0
    for right, val in enumerate(nums):
        total += val
        while val * (right - left + 1) - total > k:
            total -= nums[left]
            left += 1
        if right - left + 1 > best:
            best = right - left + 1
    return best
