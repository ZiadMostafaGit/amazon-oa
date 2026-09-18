# Two pointers: track running left/right maxima and add water at the shorter side.
from typing import List, Optional, Any


def trap(height: List[int]) -> int:
    n = len(height)
    if n < 3:
        return 0
    lo, hi = 0, n - 1
    left_max, right_max = height[lo], height[hi]
    total = 0
    while lo < hi:
        if left_max <= right_max:
            lo += 1
            if height[lo] > left_max:
                left_max = height[lo]
            else:
                total += left_max - height[lo]
        else:
            hi -= 1
            if height[hi] > right_max:
                right_max = height[hi]
            else:
                total += right_max - height[hi]
    return total
