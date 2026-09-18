# Dilworth: min strictly decreasing subsequences = longest non-decreasing subsequence (patience, O(n log n)).
from bisect import bisect_right
from typing import List, Optional, Any


def minSubsequences(nums: List[int]) -> int:
    tails = []
    for value in nums:
        pos = bisect_right(tails, value)
        if pos == len(tails):
            tails.append(value)
        else:
            tails[pos] = value
    return len(tails)
