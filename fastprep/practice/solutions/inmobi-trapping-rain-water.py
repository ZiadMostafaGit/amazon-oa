# Two-pointer scan tracking the running max from each side.
from typing import List, Optional, Any


def trapRainWater(heights: List[int]) -> int:
    if not heights:
        return 0
    left, right = 0, len(heights) - 1
    left_max = right_max = 0
    total = 0
    while left < right:
        if heights[left] <= heights[right]:
            if heights[left] >= left_max:
                left_max = heights[left]
            else:
                total += left_max - heights[left]
            left += 1
        else:
            if heights[right] >= right_max:
                right_max = heights[right]
            else:
                total += right_max - heights[right]
            right -= 1
    return total
