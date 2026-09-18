# Two-pointer in-place compaction: keep a value only if it differs from the element two slots back.
from typing import List


def solve(nums: List[int]) -> List[int]:
    k = 0
    for x in nums:
        if k < 2 or nums[k - 2] != x:
            nums[k] = x
            k += 1
    return nums[:k]
