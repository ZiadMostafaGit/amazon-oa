# Two-pointer in-place compaction over the sorted array, O(1) extra workspace.
from typing import List, Optional, Any


def deduplicateSortedArray(nums: List[int]) -> List[int]:
    write = 0
    for i in range(len(nums)):
        if write == 0 or nums[i] != nums[write - 1]:
            nums[write] = nums[i]
            write += 1
    del nums[write:]
    return nums
