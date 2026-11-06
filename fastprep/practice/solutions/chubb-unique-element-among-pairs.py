# XOR cancels pairs: x ^ x = 0 and x ^ 0 = x, so XOR of everything leaves the lone value.
from typing import List


def singleNumber(nums: List[int]) -> int:
    acc = 0
    for v in nums:
        acc ^= v
    return acc
