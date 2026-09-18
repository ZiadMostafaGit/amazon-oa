# Hash map of complement values seen so far.
from typing import List, Optional, Any


def twoSum(nums: List[int], target: int) -> List[int]:
    seen = {}
    for i, v in enumerate(nums):
        need = target - v
        if need in seen:
            return [seen[need], i]
        if v not in seen:
            seen[v] = i
    return [-1, -1]
