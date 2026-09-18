# Two-pointer in-place compaction: keep a write index, drop the (k+1)-th copy of each run.
from typing import List, Optional, Any


def keepAtMostK(nums: List[int], k: int) -> List[int]:
    if k <= 0:
        del nums[:]
        return nums
    write = 0
    for value in nums:
        if write < k or nums[write - k] != value:
            nums[write] = value
            write += 1
    del nums[write:]
    return nums
