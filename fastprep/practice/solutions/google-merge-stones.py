from typing import List, Optional, Any


def mergeStones(stones: List[int], k: int) -> int:
    n = len(stones)
    if (n - 1) % (k - 1):
        return -1
    pre = [0]
    for s in stones:
        pre.append(pre[-1] + s)
    INF = float("inf")
    # dp[i][j] = min cost to merge stones[i..j] into as few piles as possible
    dp = [[0] * n for _ in range(n)]
    for length in range(k, n + 1):
        for i in range(n - length + 1):
            j = i + length - 1
            best = INF
            for m in range(i, j, k - 1):
                c = dp[i][m] + dp[m + 1][j]
                if c < best:
                    best = c
            if (length - 1) % (k - 1) == 0:
                best += pre[j + 1] - pre[i]
            dp[i][j] = best
    return dp[0][n - 1]
