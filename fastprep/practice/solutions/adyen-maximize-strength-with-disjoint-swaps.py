# Linear DP: at each position either keep the element or swap it with its predecessor.
from typing import List, Optional, Any


def maxWeightedStrengthAfterSwaps(arr: List[int]) -> int:
    n = len(arr)
    if n == 0:
        return 0
    prev2 = 0                  # dp[i-2]
    prev1 = arr[0] * 1         # dp[1]
    if n == 1:
        return prev1
    for i in range(2, n + 1):
        keep = prev1 + arr[i - 1] * i
        swap = prev2 + arr[i - 1] * (i - 1) + arr[i - 2] * i
        cur = keep if keep > swap else swap
        prev2, prev1 = prev1, cur
    return prev1
