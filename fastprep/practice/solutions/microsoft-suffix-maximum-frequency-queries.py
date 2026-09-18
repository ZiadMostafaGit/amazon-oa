# Precompute suffix max and its count in one right-to-left pass, then answer queries in O(1).
from typing import List, Optional, Any


def suffixMaximumFrequencies(nums: List[int], queries: List[int]) -> List[int]:
    n = len(nums)
    best = [0] * n
    cnt = [0] * n
    cur_max = None
    cur_cnt = 0
    for i in range(n - 1, -1, -1):
        v = nums[i]
        if cur_max is None or v > cur_max:
            cur_max = v
            cur_cnt = 1
        elif v == cur_max:
            cur_cnt += 1
        best[i] = cur_max
        cnt[i] = cur_cnt
    return [cnt[q] for q in queries]
