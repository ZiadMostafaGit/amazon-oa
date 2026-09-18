# Monotonic increasing stack of bar indices; pop to settle each bar's maximal width.
from typing import List


def largestRectangleArea(heights: List[int]) -> int:
    stack = []  # indices with increasing heights
    best = 0
    n = len(heights)
    for i in range(n + 1):
        cur = 0 if i == n else heights[i]
        while stack and heights[stack[-1]] >= cur:
            top = stack.pop()
            left = stack[-1] if stack else -1
            area = heights[top] * (i - left - 1)
            if area > best:
                best = area
        stack.append(i)
    return best
