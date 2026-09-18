# DP over columns with per-column letter counts: dp[j] = ways to build target[:j].
from typing import List, Optional, Any


def numWays(words: List[str], target: str) -> int:
    MOD = 10 ** 9 + 7
    if not words:
        return 0
    cols = len(words[0])
    m = len(target)
    if m > cols:
        return 0

    dp = [0] * (m + 1)
    dp[0] = 1
    for col in range(cols):
        counts = [0] * 26
        for word in words:
            counts[ord(word[col]) - 97] += 1
        upper = min(m - 1, col)
        for j in range(upper, -1, -1):
            c = counts[ord(target[j]) - 97]
            if c:
                dp[j + 1] = (dp[j + 1] + dp[j] * c) % MOD
    return dp[m] % MOD
