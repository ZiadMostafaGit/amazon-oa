# Prefix/suffix products: one left-to-right pass then one right-to-left pass, no division.
from typing import List, Optional, Any


def solve(nums: List[int]) -> List[int]:
    n = len(nums)
    answer = [1] * n
    prefix = 1
    for i in range(n):
        answer[i] = prefix
        prefix *= nums[i]
    suffix = 1
    for i in range(n - 1, -1, -1):
        answer[i] *= suffix
        suffix *= nums[i]
    return answer
