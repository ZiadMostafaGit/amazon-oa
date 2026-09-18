# Linear-scan DP run twice over the circle: exclude the last house, then exclude the first.
from typing import List, Optional, Any


def _rob_line(vals: List[int]) -> int:
    take, skip = 0, 0
    for v in vals:
        take, skip = skip + v, max(skip, take)
    return max(take, skip)


def robCircular(nums: List[int]) -> int:
    n = len(nums)
    if n == 0:
        return 0
    if n == 1:
        return max(0, nums[0])
    return max(_rob_line(nums[:-1]), _rob_line(nums[1:]))
