# Gauss sum: n = len(nums) + 1, missing value = n*(n+1)//2 - sum(nums).
from typing import List, Optional, Any


def findMissingNumber(nums: List[int]) -> int:
    n = len(nums) + 1
    return n * (n + 1) // 2 - sum(nums)
