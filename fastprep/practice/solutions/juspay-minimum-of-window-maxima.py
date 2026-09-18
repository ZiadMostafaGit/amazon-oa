# Monotonic deque sliding-window maximum, tracking the minimum of those maxima.
from collections import deque
from typing import List, Optional, Any


def minimumWindowMaximum(nums: List[int], k: int) -> int:
    dq = deque()  # indices, values decreasing
    best = None
    for i, x in enumerate(nums):
        while dq and nums[dq[-1]] <= x:
            dq.pop()
        dq.append(i)
        if dq[0] <= i - k:
            dq.popleft()
        if i >= k - 1:
            m = nums[dq[0]]
            if best is None or m < best:
                best = m
    return best
