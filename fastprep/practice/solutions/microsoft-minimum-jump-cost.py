# dp[i] = cost[i] + min(dp[i-k..i-1]) with dp[0] = 0 at x = 0; the window minimum comes from a monotonic deque.
from collections import deque
from typing import List, Optional, Any


def getMinimumCost(cost: List[int], k: int) -> int:
    n = len(cost)
    dp = [0] * (n + 1)
    dq = deque([0])
    for i in range(1, n + 1):
        while dq[0] < i - k:
            dq.popleft()
        dp[i] = dp[dq[0]] + cost[i - 1]
        while dq and dp[dq[-1]] >= dp[i]:
            dq.pop()
        dq.append(i)
    return dp[n]
