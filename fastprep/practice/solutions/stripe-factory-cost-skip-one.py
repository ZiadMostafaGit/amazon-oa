# Stage-by-stage DP; each transition uses sorted positions with prefix/suffix minima of dp-pos and dp+pos to fold |x-y|.
from typing import List, Optional, Any
import bisect


def findMinimumCostThreeStages(stages: List[List[List[int]]]) -> int:
    # dp: list of (position, best cost to reach this factory)
    cur = [(p, c) for p, c in stages[0]]
    for idx in range(1, len(stages)):
        prev = sorted(cur)
        pos = [p for p, _ in prev]
        n = len(prev)
        INF = float('inf')
        pre = [INF] * n   # min(dp_j - pos_j) over j <= i
        suf = [INF] * (n + 1)  # min(dp_j + pos_j) over j >= i
        best = INF
        for j in range(n):
            v = prev[j][1] - prev[j][0]
            best = v if v < best else best
            pre[j] = best
        best = INF
        for j in range(n - 1, -1, -1):
            v = prev[j][1] + prev[j][0]
            best = v if v < best else best
            suf[j] = best
        nxt = []
        for p, c in stages[idx]:
            i = bisect.bisect_right(pos, p)
            v = INF
            if i > 0:
                v = min(v, p + pre[i - 1])
            if i < n:
                v = min(v, suf[i] - p)
            nxt.append((p, v + c))
        cur = nxt
    return int(min(c for _, c in cur))
