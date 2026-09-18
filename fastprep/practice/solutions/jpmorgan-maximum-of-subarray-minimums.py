# Sliding-window minimum with a monotonic deque, tracking the largest window minimum.
from typing import List, Optional, Any
from collections import deque


def maxOfSubarrayMinimums(arr: List[int], k: int) -> int:
    n = len(arr)
    dq = deque()  # indices with increasing values
    best = None
    for i in range(n):
        while dq and arr[dq[-1]] >= arr[i]:
            dq.pop()
        dq.append(i)
        if dq[0] <= i - k:
            dq.popleft()
        if i >= k - 1:
            cur = arr[dq[0]]
            if best is None or cur > best:
                best = cur
    return best
