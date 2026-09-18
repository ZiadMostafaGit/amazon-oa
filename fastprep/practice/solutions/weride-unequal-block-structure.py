# DP over three states per block (raise it by 0, 1 or 2 units), which always suffices to differ from both neighbours.
from typing import List


def getMinCost(heights: List[int], cost: List[int]) -> int:
    n = len(heights)
    if n <= 1:
        return 0
    INF = float('inf')
    dp = [0, cost[0], 2 * cost[0]]
    prev_h = heights[0]
    for i in range(1, n):
        h = heights[i]
        c = cost[i]
        nd = [INF, INF, INF]
        for d in range(3):
            fin = h + d
            best = INF
            for pd in range(3):
                if prev_h + pd != fin and dp[pd] < best:
                    best = dp[pd]
            if best < INF:
                nd[d] = best + d * c
        dp = nd
        prev_h = h
    return int(min(dp))
