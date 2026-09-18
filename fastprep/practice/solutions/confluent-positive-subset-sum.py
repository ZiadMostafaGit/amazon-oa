# Bitset subset-sum DP: track reachable sums as bits of a big integer.
from typing import List


def canReachTarget(nums: List[int], target: int) -> bool:
    if target <= 0:
        return target == 0
    mask = (1 << (target + 1)) - 1
    reach = 1  # bit i set == sum i reachable
    for v in nums:
        if v > target:
            continue
        reach |= (reach << v) & mask
        if (reach >> target) & 1:
            return True
    return bool((reach >> target) & 1)
