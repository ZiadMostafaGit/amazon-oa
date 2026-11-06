# BFS by layers over a range: track the furthest reach of the current jump window.
from typing import List, Optional, Any


def jump(nums: List[int]) -> int:
    jumps = 0
    end = 0
    far = 0
    for i in range(len(nums) - 1):
        far = max(far, i + nums[i])
        if i == end:
            jumps += 1
            end = far
            if end >= len(nums) - 1:
                break
    return jumps
