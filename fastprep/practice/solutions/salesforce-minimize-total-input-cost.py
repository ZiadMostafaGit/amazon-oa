# DP over (weeks used, prefix length), extending the last week's running maximum backwards.
from typing import List, Optional, Any


def minimizeTotalInputCost(campaignCosts: List[int], numberOfWeeks: int) -> int:
    n = len(campaignCosts)
    INF = float('inf')
    # dp[i] = min total cost covering the first i campaigns with the weeks processed so far
    dp = [INF] * (n + 1)
    dp[0] = 0
    for week in range(1, numberOfWeeks + 1):
        nxt = [INF] * (n + 1)
        for i in range(week, n - (numberOfWeeks - week) + 1):
            best = INF
            running_max = 0
            # last week covers campaigns j..i-1
            for j in range(i - 1, week - 2, -1):
                if campaignCosts[j] > running_max:
                    running_max = campaignCosts[j]
                if dp[j] < INF:
                    candidate = dp[j] + running_max
                    if candidate < best:
                        best = candidate
            nxt[i] = best
        dp = nxt
    return dp[n]
