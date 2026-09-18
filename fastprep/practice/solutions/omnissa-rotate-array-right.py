# Slicing: right rotation by k is the last k%n elements followed by the rest.
from typing import List, Optional, Any


def rotateRight(nums: List[int], k: int) -> List[int]:
    n = len(nums)
    if n == 0:
        return []
    k %= n
    if k == 0:
        return list(nums)
    return list(nums[-k:]) + list(nums[:-k])
