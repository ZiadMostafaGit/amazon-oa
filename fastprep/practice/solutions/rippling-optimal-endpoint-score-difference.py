# Game DP on intervals: d[i][j] = best (mover - opponent) on nums[i..j] = max(nums[i] - d[i+1][j], nums[j] - d[i][j-1]).
from typing import List


def maximumScoreDifference(nums: List[int]) -> int:
    n = len(nums)
    d = list(nums)                      # length-1 intervals: d[i] = nums[i]
    for length in range(2, n + 1):
        for i in range(n - length + 1):
            j = i + length - 1
            # d[i] currently holds interval i..j-1, d[i+1] holds i+1..j
            d[i] = max(nums[i] - d[i + 1], nums[j] - d[i])
    return d[0]
