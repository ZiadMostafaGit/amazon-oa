# Two pointers from both ends, moving the shorter side inward.
from typing import List, Optional, Any


def solve(height: List[int]) -> int:
    i, j = 0, len(height) - 1
    best = 0
    while i < j:
        h = height[i] if height[i] < height[j] else height[j]
        area = h * (j - i)
        if area > best:
            best = area
        if height[i] < height[j]:
            i += 1
        else:
            j -= 1
    return best
