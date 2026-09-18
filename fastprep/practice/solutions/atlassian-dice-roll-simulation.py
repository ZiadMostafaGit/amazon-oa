# DP on (last face, current run length) with a running total to fold all "switch face" transitions.
from typing import List

MOD = 1000000007


def dieSimulator(n: int, rollMax: List[int]) -> int:
    # dp[j][c] = sequences ending with face j repeated c+1 times
    dp = [[0] * rollMax[j] for j in range(6)]
    for j in range(6):
        dp[j][0] = 1
    total = 6
    for _ in range(n - 1):
        ends = [sum(dp[j]) % MOD for j in range(6)]
        ndp = [[0] * rollMax[j] for j in range(6)]
        ntotal = 0
        for j in range(6):
            fresh = (total - ends[j]) % MOD
            ndp[j][0] = fresh
            row, nrow = dp[j], ndp[j]
            for c in range(1, rollMax[j]):
                nrow[c] = row[c - 1]
            ntotal = (ntotal + sum(nrow)) % MOD
        dp = ndp
        total = ntotal
    return total % MOD
