# Monotonic deque sliding-window minimum, tracking the maximum of those minimums.
from typing import List, Optional, Any
from collections import deque


def maximumOfWindowMinimums(nums: List[int], windowSize: int) -> int:
    dq = deque()  # indices, values increasing
    best = None
    for i, v in enumerate(nums):
        while dq and nums[dq[-1]] >= v:
            dq.pop()
        dq.append(i)
        if dq[0] <= i - windowSize:
            dq.popleft()
        if i >= windowSize - 1:
            cur = nums[dq[0]]
            if best is None or cur > best:
                best = cur
    return best
