# DP over columns: snake through a prefix of columns, then U-turn out to the last column and back.
from typing import List, Optional, Any

NEG = float('-inf')


def maxTimedCoins(coins: List[List[int]]) -> int:
    top = coins[0]
    bot = coins[1]
    n = len(top)
    rows = (top, bot)

    # Suffix sums: S[r][i] = sum of coins[r][i:], T[r][i] = sum of j*coins[r][j] for j >= i.
    S = [[0] * (n + 1), [0] * (n + 1)]
    T = [[0] * (n + 1), [0] * (n + 1)]
    for r in (0, 1):
        row = rows[r]
        Sr = S[r]
        Tr = T[r]
        for j in range(n - 1, -1, -1):
            Sr[j] = Sr[j + 1] + row[j]
            Tr[j] = Tr[j + 1] + j * row[j]

    def uturn(i: int, r: int) -> int:
        o = 1 - r
        return i * S[r][i] + T[r][i] + (i + 2 * n - 1) * S[o][i] - T[o][i]

    # dp[r] = best score having fully covered columns 0..i-1 and standing on (r, i-1) at time 2i-1.
    dp0, dp1 = 0, NEG  # i = 0: standing at the start cell (0,0) at time 0, nothing collected.
    best = uturn(0, 0)

    for i in range(n):
        if dp0 != NEG:
            cand = dp0 + uturn(i, 0) if i > 0 else NEG
            if cand > best:
                best = cand
        if dp1 != NEG:
            cand = dp1 + uturn(i, 1)
            if cand > best:
                best = cand
        # Snake across column i: (r, i) at time 2i, then (1-r, i) at time 2i+1.
        a = 2 * i * top[i] + (2 * i + 1) * bot[i]
        b = 2 * i * bot[i] + (2 * i + 1) * top[i]
        ndp0 = dp1 + b if dp1 != NEG else NEG   # was on bottom, ends on top
        ndp1 = dp0 + a if dp0 != NEG else NEG   # was on top, ends on bottom
        dp0, dp1 = ndp0, ndp1

    for v in (dp0, dp1):
        if v != NEG and v > best:
            best = v
    return int(best)
