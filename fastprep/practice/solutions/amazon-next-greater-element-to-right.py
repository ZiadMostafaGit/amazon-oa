# Monotonic stack scanned from the right: pop everything <= the current value; the top is its answer.
from typing import List


def nextGreaterToRight(nums: List[int]) -> List[int]:
    n = len(nums)
    res = [-1] * n
    stack = []  # values, strictly decreasing from bottom to top
    for i in range(n - 1, -1, -1):
        while stack and stack[-1] <= nums[i]:
            stack.pop()
        if stack:
            res[i] = stack[-1]
        stack.append(nums[i])
    return res
