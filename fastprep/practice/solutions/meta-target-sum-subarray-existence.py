# Prefix sums in a hash set: a subarray sums to target iff some earlier prefix equals running - target.
from typing import List, Optional, Any


def hasTargetSumSubarray(nums: List[int], target: int) -> bool:
    seen = {0}
    running = 0
    for v in nums:
        running += v
        if running - target in seen:
            return True
        seen.add(running)
    return False
