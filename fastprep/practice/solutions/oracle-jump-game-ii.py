# Greedy BFS-by-levels: extend the current reachable frontier, counting one jump per level.
from typing import List, Optional, Any


def jump(nums: List[int]) -> int:
    n = len(nums)
    if n <= 1:
        return 0
    jumps = 0
    current_end = 0
    farthest = 0
    for i in range(n - 1):
        if i + nums[i] > farthest:
            farthest = i + nums[i]
        if i == current_end:
            jumps += 1
            current_end = farthest
            if current_end >= n - 1:
                break
    return jumps
