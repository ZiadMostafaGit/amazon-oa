# Linear dynamic programming with two rolling states (take / skip).
from typing import List, Optional, Any


def rob(nums: List[int]) -> int:
    prev, cur = 0, 0
    for x in nums:
        prev, cur = cur, max(cur, prev + x)
    return cur
