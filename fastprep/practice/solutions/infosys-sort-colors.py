# Counting sort: only three values, so count each, then overwrite the array in order. O(n), O(1) extra.
from typing import List, Optional, Any


def sortColors(nums: List[int]) -> List[int]:
    count = [0, 0, 0]
    for x in nums:
        count[x] += 1
    i = 0
    for color in range(3):
        for _ in range(count[color]):
            nums[i] = color
            i += 1
    return nums
