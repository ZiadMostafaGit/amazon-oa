# Sliding window with two monotonic deques tracking window max and min.
from typing import List, Optional, Any
from collections import deque


def longestSubarrayWithinLimit(nums: List[int], limit: int) -> int:
    if not nums:
        return 0
    max_dq = deque()  # decreasing values
    min_dq = deque()  # increasing values
    left = 0
    best = 0
    for right, val in enumerate(nums):
        while max_dq and nums[max_dq[-1]] <= val:
            max_dq.pop()
        max_dq.append(right)
        while min_dq and nums[min_dq[-1]] >= val:
            min_dq.pop()
        min_dq.append(right)
        while nums[max_dq[0]] - nums[min_dq[0]] > limit:
            if max_dq[0] == left:
                max_dq.popleft()
            if min_dq[0] == left:
                min_dq.popleft()
            left += 1
        if right - left + 1 > best:
            best = right - left + 1
    return best
