# Two-pointer sweep inward, always moving the shorter side.
from typing import List, Optional, Any


def maxArea(heights: List[int]) -> int:
    left = 0
    right = len(heights) - 1
    best = 0
    while left < right:
        h = heights[left] if heights[left] < heights[right] else heights[right]
        area = (right - left) * h
        if area > best:
            best = area
        if heights[left] < heights[right]:
            left += 1
        else:
            right -= 1
    return best
