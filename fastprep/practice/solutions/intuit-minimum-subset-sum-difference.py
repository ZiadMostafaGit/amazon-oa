# Reachable subset sums; the best split puts one group as close to total/2 from below as possible.
from typing import List


def minimumDifference(nums: List[int]) -> int:
    total = sum(nums)
    half = total // 2
    mask = (1 << (half + 1)) - 1
    reach = 1
    for v in nums:
        reach |= (reach << v) & mask
    s = reach.bit_length() - 1            # largest reachable sum <= total/2
    return total - 2 * s
