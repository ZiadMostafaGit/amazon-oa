# Patience sorting: binary-search tails array, O(n log n).
from typing import List, Optional, Any
from bisect import bisect_left


def lengthOfLIS(nums: List[int]) -> int:
    tails = []
    for x in nums:
        i = bisect_left(tails, x)  # strict increase -> replace first >= x
        if i == len(tails):
            tails.append(x)
        else:
            tails[i] = x
    return len(tails)
