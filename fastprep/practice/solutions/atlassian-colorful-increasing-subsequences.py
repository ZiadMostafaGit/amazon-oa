# DP over (last index, color bitmask): extend every increasing subsequence ending earlier.
from typing import List, Optional, Any


def countColorfulSubsequences(heights: List[int], colors: List[int], k: int) -> int:
    MOD = 10 ** 9 + 7
    n = len(heights)
    full = (1 << k) - 1
    size = 1 << k
    dp = [[0] * size for _ in range(n)]

    for i in range(n):
        bit = 1 << (colors[i] - 1)
        row = dp[i]
        row[bit] = (row[bit] + 1) % MOD
        hi = heights[i]
        for j in range(i):
            if heights[j] < hi:
                prev = dp[j]
                for mask in range(size):
                    v = prev[mask]
                    if v:
                        nm = mask | bit
                        row[nm] = (row[nm] + v) % MOD

    total = 0
    for i in range(n):
        total = (total + dp[i][full]) % MOD
    return total
