# Two-pointer sweep from both ends, always moving the shorter line inward.
from typing import List, Optional, Any


def maxArea(height: List[int]) -> int:
    lo, hi = 0, len(height) - 1
    best = 0
    while lo < hi:
        h = height[lo] if height[lo] < height[hi] else height[hi]
        area = h * (hi - lo)
        if area > best:
            best = area
        if height[lo] < height[hi]:
            lo += 1
        else:
            hi -= 1
    return best
