# Classic unbounded-knapsack counting DP, coin loop outermost for unordered combos.
from typing import List


def countCombinations(coins: List[int], target: int) -> int:
    dp = [0] * (target + 1)
    dp[0] = 1
    for c in coins:
        if c > target:
            continue
        for s in range(c, target + 1):
            dp[s] += dp[s - c]
    return dp[target]
