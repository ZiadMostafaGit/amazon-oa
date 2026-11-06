# After step i with l picks from the left, the right end is fixed: dp over (step, left picks), O(m^2).
from typing import List


def maximumWeightedEndScore(nums: List[int], multipliers: List[int]) -> int:
    n, m = len(nums), len(multipliers)
    dp = [0] * (m + 1)                  # dp[l] = best score from step i on, given l left picks so far
    for i in range(m - 1, -1, -1):
        mul = multipliers[i]
        new = [0] * (i + 1)
        for l in range(i + 1):
            r = n - 1 - (i - l)
            a = mul * nums[l] + dp[l + 1]
            b = mul * nums[r] + dp[l]
            new[l] = a if a > b else b
        dp = new
    return dp[0]
