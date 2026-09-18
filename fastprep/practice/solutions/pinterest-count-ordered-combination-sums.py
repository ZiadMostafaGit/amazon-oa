# Combination-sum-IV style DP: dp[t] = sum of dp[t - c] over candidates.
from typing import List, Optional, Any


def countOrderedCombinationSums(candidates: List[int], target: int) -> int:
    dp = [0] * (target + 1)
    dp[0] = 1
    for t in range(1, target + 1):
        total = 0
        for c in candidates:
            if c <= t:
                total += dp[t - c]
        dp[t] = total
    return dp[target]
