# Single pass tracking the minimum prefix value seen so far.
from typing import List, Optional, Any


def maximumDifference(nums: List[int]) -> int:
    best = -1
    mn = nums[0] if nums else 0
    for j in range(1, len(nums)):
        v = nums[j]
        if v >= mn:
            d = v - mn
            if d > best:
                best = d
        elif v < mn:
            mn = v
    return best
