# DP over compressed candidate values with running prefix minima, run once forward and once on the reversed array.
from typing import List, Optional, Any


def _best_non_decreasing(arr: List[int], vals: List[int]) -> int:
    m = len(vals)
    dp = [abs(arr[0] - v) for v in vals]
    for i in range(1, len(arr)):
        a = arr[i]
        run = dp[0]
        nxt = [0] * m
        for j in range(m):
            if dp[j] < run:
                run = dp[j]
            nxt[j] = run + abs(a - vals[j])
        dp = nxt
    return min(dp)


def minMonotonicCost(arr: List[int]) -> int:
    vals = sorted(set(arr))
    up = _best_non_decreasing(arr, vals)
    down = _best_non_decreasing(arr[::-1], vals)
    return min(up, down)
