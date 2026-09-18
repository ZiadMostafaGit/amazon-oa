# Two-dimensional 0/1 knapsack on (ones used, zeroes used).
from typing import List, Optional, Any


def solve(strs: List[str], maxOnes: int, maxZeroes: int) -> int:
    if maxOnes < 0 or maxZeroes < 0:
        return 0
    dp = [[0] * (maxZeroes + 1) for _ in range(maxOnes + 1)]
    for w in strs:
        ones = w.count('1')
        zeros = len(w) - ones
        if ones > maxOnes or zeros > maxZeroes:
            continue
        for o in range(maxOnes, ones - 1, -1):
            row = dp[o]
            src = dp[o - ones]
            for z in range(maxZeroes, zeros - 1, -1):
                cand = src[z - zeros] + 1
                if cand > row[z]:
                    row[z] = cand
    return dp[maxOnes][maxZeroes]
