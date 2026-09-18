# Approach: prefix sums with a monotonic deque holding the minimum prefix within the last k positions.
from collections import deque
from typing import List, Optional, Any


def maxSubarrayAtMostK(nums: List[int], k: int) -> int:
    n = len(nums)
    prefix = [0] * (n + 1)
    for i, v in enumerate(nums):
        prefix[i + 1] = prefix[i] + v

    best = None
    dq = deque([0])  # indices into prefix, increasing prefix values
    for i in range(1, n + 1):
        while dq and dq[0] < i - k:
            dq.popleft()
        cand = prefix[i] - prefix[dq[0]]
        if best is None or cand > best:
            best = cand
        while dq and prefix[dq[-1]] >= prefix[i]:
            dq.pop()
        dq.append(i)
    return best
