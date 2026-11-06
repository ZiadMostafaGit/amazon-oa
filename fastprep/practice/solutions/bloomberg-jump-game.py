from typing import List, Optional, Any


def canJump(nums: List[int]) -> bool:
    reach = 0
    for i, v in enumerate(nums):
        if i > reach:
            return False
        reach = max(reach, i + v)
    return True
