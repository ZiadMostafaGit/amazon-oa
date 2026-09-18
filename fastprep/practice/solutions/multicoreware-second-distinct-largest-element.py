# Track the two largest distinct values in a single pass.
from typing import List, Optional, Any


def secondLargestDistinct(nums: List[int]) -> int:
    best = None
    second = None
    for v in nums:
        if best is None or v > best:
            if best is not None and (second is None or best > second):
                second = best
            best = v
        elif v != best and (second is None or v > second):
            second = v
    return second
