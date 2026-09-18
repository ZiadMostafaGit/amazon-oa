# DP over word columns: dp[j] = ways to build target prefix j, times per-column letter counts.
from typing import List, Optional, Any


def numWays(words: List[str], target: str) -> int:
    MOD = 10 ** 9 + 7
    if not words:
        return 0
    m = len(target)
    width = len(words[0])
    if m > width:
        return 0

    dp = [0] * (m + 1)
    dp[0] = 1
    for col in range(width):
        counts = {}
        for w in words:
            ch = w[col]
            counts[ch] = counts.get(ch, 0) + 1
        # go backwards so each column is used at most once per construction
        upper = min(col, m - 1)
        for j in range(upper, -1, -1):
            c = counts.get(target[j], 0)
            if c and dp[j]:
                dp[j + 1] = (dp[j + 1] + dp[j] * c) % MOD
    return dp[m] % MOD
