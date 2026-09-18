# Approach: hash set, expand a run only from values that start one (v-1 absent) -> O(n).
from typing import List, Optional, Any


def solve(nums: List[int]) -> int:
    seen = set(nums)
    best = 0
    for v in seen:
        if v - 1 in seen:
            continue
        cur = v
        length = 1
        while cur + 1 in seen:
            cur += 1
            length += 1
        if length > best:
            best = length
    return best
