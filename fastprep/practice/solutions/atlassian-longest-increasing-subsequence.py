# Patience sorting: binary-search tails array for O(n log n) longest strictly increasing subsequence.
from typing import List, Optional, Any
from bisect import bisect_left


def lengthOfLIS(nums: List[int]) -> int:
    tails: List[int] = []
    for v in nums:
        i = bisect_left(tails, v)
        if i == len(tails):
            tails.append(v)
        else:
            tails[i] = v
    return len(tails)
