# Linear DP: dp[i] = ratings[i] + max(dp[i-1], dp[i-2]) since at most one movie may be skipped in a row.
from typing import List, Optional, Any


def maximizeRatings(ratings: List[int]) -> int:
    n = len(ratings)
    if n == 0:
        return 0
    if n == 1:
        return ratings[0]

    prev2 = 0          # best sum taking index i-2 (0 means nothing taken yet)
    prev1 = ratings[0]  # best sum taking index i-1
    for i in range(1, n):
        cur = ratings[i] + (prev1 if prev1 > prev2 else prev2)
        prev2, prev1 = prev1, cur
    return prev1 if prev1 > prev2 else prev2
