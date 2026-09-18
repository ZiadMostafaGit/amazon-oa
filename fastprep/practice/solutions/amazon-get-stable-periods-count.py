# Sliding window counting subarrays with at most k distinct values; add window length at each right end.
from typing import List, Optional, Any


def getStablePeriodsCount(revenues: List[int], k: int) -> int:
    MOD = 10 ** 9 + 7
    counts = {}
    left = 0
    total = 0
    for right, v in enumerate(revenues):
        counts[v] = counts.get(v, 0) + 1
        while len(counts) > k:
            lv = revenues[left]
            counts[lv] -= 1
            if counts[lv] == 0:
                del counts[lv]
            left += 1
        total += right - left + 1
    return total % MOD
