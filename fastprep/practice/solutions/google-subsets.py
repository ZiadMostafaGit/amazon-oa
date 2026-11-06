# A bitmask is a set: mask in 0..2^n-1, bit i set means nums[i] is in the subset.
from typing import List


def subsets(nums: List[int]) -> List[List[int]]:
    n = len(nums)
    out = []
    for mask in range(1 << n):
        out.append([nums[i] for i in range(n) if mask >> i & 1])
    return out
