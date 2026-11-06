# Circular next greater: walk the array twice, keeping a stack of indices still waiting for an answer.
from typing import List


def nextGreaterElements(nums: List[int]) -> List[int]:
    n = len(nums)
    res = [-1] * n
    stack = []  # indices whose values decrease from bottom to top
    for j in range(2 * n):
        i = j % n
        while stack and nums[stack[-1]] < nums[i]:
            res[stack.pop()] = nums[i]
        if j < n:
            stack.append(i)
    return res
