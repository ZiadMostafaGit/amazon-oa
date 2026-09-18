# Two-pointer sweep tracking the running left and right maxima.
from typing import List, Optional, Any


def solve(height: List[int]) -> int:
    if not height:
        return 0
    left, right = 0, len(height) - 1
    left_max, right_max = height[left], height[right]
    total = 0

    while left < right:
        if left_max <= right_max:
            left += 1
            if height[left] > left_max:
                left_max = height[left]
            else:
                total += left_max - height[left]
        else:
            right -= 1
            if height[right] > right_max:
                right_max = height[right]
            else:
                total += right_max - height[right]

    return total
