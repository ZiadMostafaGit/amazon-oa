# XOR of all = a ^ b; its lowest set bit differs between a and b, so split by that bit and XOR each half.
from typing import List


def findTwoUniqueNumbers(nums: List[int]) -> List[int]:
    x = 0
    for v in nums:
        x ^= v
    low = x & -x
    a = 0
    for v in nums:
        if v & low:
            a ^= v
    b = x ^ a
    return sorted([a, b])
