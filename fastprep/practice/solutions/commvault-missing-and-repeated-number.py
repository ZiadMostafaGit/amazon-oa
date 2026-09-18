# Math identities: sum and sum-of-squares differences give (r - m) and (r + m) in O(n) time, O(1) space.
from typing import List, Optional, Any


def findRepeatedAndMissing(nums: List[int]) -> List[int]:
    n = len(nums)
    total = 0
    total_sq = 0
    for v in nums:
        total += v
        total_sq += v * v
    expected = n * (n + 1) // 2
    expected_sq = n * (n + 1) * (2 * n + 1) // 6
    diff = total - expected            # r - m
    diff_sq = total_sq - expected_sq   # r^2 - m^2 = (r - m)(r + m)
    s = diff_sq // diff                # r + m
    repeated = (s + diff) // 2
    missing = (s - diff) // 2
    return [repeated, missing]
