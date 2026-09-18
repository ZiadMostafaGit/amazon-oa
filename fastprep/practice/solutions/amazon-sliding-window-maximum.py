# Monotonic decreasing deque of indices, O(n).
from typing import List, Optional, Any
from collections import deque


def maxSlidingWindow(nums: List[int], k: int) -> List[int]:
    n = len(nums)
    if n == 0 or k <= 0:
        return []
    k = min(k, n)
    dq = deque()
    out = []
    for i, v in enumerate(nums):
        while dq and nums[dq[-1]] <= v:
            dq.pop()
        dq.append(i)
        if dq[0] <= i - k:
            dq.popleft()
        if i >= k - 1:
            out.append(nums[dq[0]])
    return out
