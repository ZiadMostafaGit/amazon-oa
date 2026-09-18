# Approach: row-by-row DP for the minimum falling path sum, subtracted from the starting power.
from typing import List


def maxPower(city: List[List[int]]) -> int:
    if not city or not city[0]:
        return 100
    cols = len(city[0])
    dp = list(city[0])
    for r in range(1, len(city)):
        nxt = [0] * cols
        for c in range(cols):
            best = dp[c]
            if c > 0 and dp[c - 1] < best:
                best = dp[c - 1]
            if c + 1 < cols and dp[c + 1] < best:
                best = dp[c + 1]
            nxt[c] = best + city[r][c]
        dp = nxt
    return 100 - min(dp)
