# Monotonic increasing stack: pop bars to compute the maximal width for each height.
from typing import List, Optional, Any


def largestRectangleArea(heights: List[int]) -> int:
    stack = []  # indices with increasing heights
    best = 0
    n = len(heights)
    for i in range(n + 1):
        h = 0 if i == n else heights[i]
        while stack and heights[stack[-1]] >= h:
            top = stack.pop()
            left = stack[-1] + 1 if stack else 0
            area = heights[top] * (i - left)
            if area > best:
                best = area
        stack.append(i)
    return best
