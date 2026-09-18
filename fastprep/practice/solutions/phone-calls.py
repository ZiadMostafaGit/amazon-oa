# Weighted interval scheduling: sort by end time, DP with binary search for last compatible call.
from bisect import bisect_right
from typing import List, Optional, Any


def phoneCalls(start: List[int], duration: List[int], volume: List[int]) -> int:
    n = len(start)
    calls = sorted(
        ((start[i] + duration[i], start[i], volume[i]) for i in range(n))
    )
    ends = [c[0] for c in calls]
    dp = [0] * (n + 1)
    for i in range(n):
        end_i, start_i, vol_i = calls[i]
        # last call whose end <= start_i
        j = bisect_right(ends, start_i, 0, i)
        dp[i + 1] = max(dp[i], dp[j] + vol_i)
    return dp[n]
