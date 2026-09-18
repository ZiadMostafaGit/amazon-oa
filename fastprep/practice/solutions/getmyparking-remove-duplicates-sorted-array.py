# Two-pointer in-place compaction of a sorted array.
from typing import List, Optional, Any


def removeDuplicates(nums: List[int]) -> List[int]:
    if not nums:
        return []
    k = 1
    for i in range(1, len(nums)):
        if nums[i] != nums[k - 1]:
            nums[k] = nums[i]
            k += 1
    return nums[:k]
