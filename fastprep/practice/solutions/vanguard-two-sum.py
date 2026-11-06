# One pass with value -> index: for each x, look up its complement target - x among earlier values. O(n).
from typing import List, Optional, Any


def twoSum(nums: List[int], target: int) -> List[int]:
    index_of = {}
    for j, x in enumerate(nums):
        i = index_of.get(target - x)
        if i is not None:
            return [i, j]
        if x not in index_of:
            index_of[x] = j
    return []
