# Bipartition invariant + Scoins' formula a^(b-1)*b^(a-1), counted by subset-sum DP.
from typing import List, Optional, Any

MOD = 1000000007


def countStableTrees(workloads: List[int]) -> int:
    n = len(workloads)
    if n == 1:
        return 1 if workloads[0] == 1 else 0
    # Distance-2 moves keep every unit inside its side of the tree's bipartition,
    # and inside a side all vertices are linked by distance-2 steps, so a tree is
    # stable exactly when each side's workload equals its size.
    # Count subsets by size whose sum of (w_i - 1) is zero.
    LO, HI = -n, n  # sums outside this window can never return to 0
    width = HI - LO + 1
    # dp[k][s - LO] = number of subsets of size k with shifted sum s
    dp = [[0] * width for _ in range(n + 1)]
    dp[0][-LO] = 1
    for w in workloads:
        v = w - 1
        for k in range(min(n, n) - 1, -1, -1):
            row = dp[k]
            nxt = dp[k + 1]
            for s in range(width):
                c = row[s]
                if c:
                    ns = s + v
                    if 0 <= ns < width:
                        nxt[ns] = (nxt[ns] + c) % MOD
    total = 0
    for k in range(1, n):
        cnt = dp[k][-LO]
        if cnt:
            b = n - k
            total = (total + cnt * pow(k, b - 1, MOD) % MOD * pow(b, k - 1, MOD)) % MOD
    # each tree was counted once per ordered choice of side
    return total * pow(2, MOD - 2, MOD) % MOD
