# Hash set of the smaller array, then scan the other for target - value.
from typing import List, Optional, Any


def hasCrossArrayTargetSum(first: List[int], second: List[int], target: int) -> bool:
    if not first or not second:
        return False
    if len(first) > len(second):
        first, second = second, first
    seen = set(first)
    for v in second:
        if target - v in seen:
            return True
    return False
