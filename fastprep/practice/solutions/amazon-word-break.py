# Approach: classic DP over prefixes, checking each dictionary word length at every position.
from typing import List


def solve(s: str, wordDict: List[str]) -> bool:
    words = set(wordDict)
    lengths = sorted({len(w) for w in words})
    n = len(s)
    dp = [False] * (n + 1)
    dp[0] = True
    for i in range(1, n + 1):
        for L in lengths:
            if L > i:
                break
            if dp[i - L] and s[i - L:i] in words:
                dp[i] = True
                break
    return dp[n]
