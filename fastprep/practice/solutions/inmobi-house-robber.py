# Linear dynamic programming with two rolling states (best including / excluding the current house).
from typing import List, Optional, Any


def rob(nums: List[int]) -> int:
    take = 0
    skip = 0
    for value in nums:
        take, skip = skip + value, max(skip, take)
    return max(take, skip)
