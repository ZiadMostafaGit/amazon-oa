from typing import List, Optional, Any
from bisect import bisect_left


def longestSubarrayAtMostK(nums: List[int], k: int) -> int:
    # sum(nums[j:i]) = P[i] - P[j] <= k  <=>  P[j] >= P[i] - k.
    # The running maximum of prefix sums is non-decreasing, so the earliest j
    # with P[j] >= target is found by binary search on it.
    runmax = [0]  # runmax[j] = max(P[0..j])
    p = 0
    best = 0
    for i, x in enumerate(nums, 1):
        p += x
        j = bisect_left(runmax, p - k)
        if j < i and i - j > best:
            best = i - j
        runmax.append(p if p > runmax[-1] else runmax[-1])
    return best
