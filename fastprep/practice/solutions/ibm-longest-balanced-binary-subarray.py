# Longest-valid-parentheses stack scan with 1 as an opener and 0 as a closer.
from typing import List, Optional, Any


def longestBalancedBinarySubarray(arr: List[int]) -> int:
    stack = [-1]
    best = 0
    for i, v in enumerate(arr):
        if v == 1:
            stack.append(i)
        else:
            stack.pop()
            if not stack:
                stack.append(i)
            else:
                span = i - stack[-1]
                if span > best:
                    best = span
    return best
