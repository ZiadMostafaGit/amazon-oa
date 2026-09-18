# Linear DP over prefixes: dp[i] = cheapest decoding of digits[:i] via a 1- or 2-digit chunk.
from typing import List, Optional, Any


def minDecodingCost(digits: str, letterCosts: List[int]) -> int:
    n = len(digits)
    INF = float("inf")
    dp = [INF] * (n + 1)
    dp[0] = 0
    for i in range(1, n + 1):
        one = ord(digits[i - 1]) - 48
        if one >= 1 and dp[i - 1] < INF:
            cand = dp[i - 1] + letterCosts[one - 1]
            if cand < dp[i]:
                dp[i] = cand
        if i >= 2 and digits[i - 2] != '0':
            two = (ord(digits[i - 2]) - 48) * 10 + one
            if 1 <= two <= 26 and dp[i - 2] < INF:
                cand = dp[i - 2] + letterCosts[two - 1]
                if cand < dp[i]:
                    dp[i] = cand
    return -1 if dp[n] == INF else dp[n]
