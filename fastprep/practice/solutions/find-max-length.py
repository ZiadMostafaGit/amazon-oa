# DP over positions x transitions: dp[i][j] = best subsequence ending at i using j unequal adjacent pairs.
from typing import List, Optional, Any


def findMaxLength(skills: List[int], k: int) -> int:
    n = len(skills)
    if n == 0:
        return 0
    if k < 0:
        k = 0
    if k > n - 1:
        k = n - 1

    # Compress skill values to dense ids.
    ids = {}
    comp = []
    for v in skills:
        if v not in ids:
            ids[v] = len(ids)
        comp.append(ids[v])
    d = len(ids)

    NEG = -1
    # best_same[j][v] = max dp[p][j] over processed p with comp[p] == v
    best_same = [[NEG] * d for _ in range(k + 1)]
    # best_any[j] = max dp[p][j] over all processed p
    best_any = [NEG] * (k + 1)

    ans = 1
    cur = [0] * (k + 1)
    for i in range(n):
        v = comp[i]
        for j in range(k + 1):
            val = 1
            bs = best_same[j][v]
            if bs > 0 and bs + 1 > val:
                val = bs + 1
            if j > 0:
                ba = best_any[j - 1]
                if ba > 0 and ba + 1 > val:
                    val = ba + 1
            cur[j] = val
            if val > ans:
                ans = val
        for j in range(k + 1):
            val = cur[j]
            if val > best_same[j][v]:
                best_same[j][v] = val
            if val > best_any[j]:
                best_any[j] = val
    return ans
