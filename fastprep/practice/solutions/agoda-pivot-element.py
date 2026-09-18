# Prefix maximum and suffix minimum scan over internal indices.
from typing import List, Optional, Any


def findPivotElement(nums: List[int]) -> int:
    n = len(nums)
    if n < 3:
        return -1
    suffix_min = [0] * n
    suffix_min[n - 1] = nums[n - 1]
    for i in range(n - 2, -1, -1):
        suffix_min[i] = min(nums[i], suffix_min[i + 1])
    prefix_max = nums[0]
    for i in range(1, n - 1):
        if prefix_max < nums[i] < suffix_min[i + 1]:
            return nums[i]
        if nums[i] > prefix_max:
            prefix_max = nums[i]
    return -1
