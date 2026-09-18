# Dynamic programming: dp[i] = min over last-block length j<=threshold of dp[i-j] + max(arr[i-j:i]).
from typing import List, Optional, Any


def efficientCost(arr: List[int], threshold: int) -> int:
    n = len(arr)
    if n == 0:
        return 0
    if threshold <= 0:
        return -1
    INF = float('inf')
    dp = [INF] * (n + 1)
    dp[0] = 0
    for i in range(1, n + 1):
        best = INF
        cur_max = 0
        for j in range(1, min(threshold, i) + 1):
            v = arr[i - j]
            if v > cur_max:
                cur_max = v
            if dp[i - j] + cur_max < best:
                best = dp[i - j] + cur_max
        dp[i] = best
    return int(dp[n])
