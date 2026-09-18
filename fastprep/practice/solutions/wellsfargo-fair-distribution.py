# Enumerate every circular cut point, and for each candidate minimum part sum run a DP that
# minimizes the maximum part; keep the partition with the smallest (max - min) spread.
from typing import List, Optional, Any


def allocateWells(A: List[int], N: int) -> List[int]:
    n = len(A)
    if n == 0 or N <= 0:
        return []
    if N == 1:
        return [sum(A)]
    if N >= n:
        return list(A)

    total = sum(A)
    INF = float("inf")

    def solve_linear(b: List[int], L: int):
        """Split b into N contiguous non-empty parts, each with sum >= L,
        minimizing the largest part. Returns (maxpart, cuts) or None."""
        m = len(b)
        pre = [0] * (m + 1)
        for i, v in enumerate(b):
            pre[i + 1] = pre[i] + v
        # f[k][i] = min possible max over first i elements split into k parts
        f = [[INF] * (m + 1) for _ in range(N + 1)]
        par = [[-1] * (m + 1) for _ in range(N + 1)]
        f[0][0] = 0
        for k in range(1, N + 1):
            for i in range(k, m - (N - k) + 1):
                best = INF
                bestj = -1
                for j in range(k - 1, i):
                    if f[k - 1][j] == INF:
                        continue
                    seg = pre[i] - pre[j]
                    if seg < L:
                        continue
                    cand = f[k - 1][j] if f[k - 1][j] > seg else seg
                    if cand < best:
                        best = cand
                        bestj = j
                f[k][i] = best
                par[k][i] = bestj
        if f[N][m] == INF:
            return None
        cuts = []
        i = m
        for k in range(N, 0, -1):
            j = par[k][i]
            cuts.append((j, i))
            i = j
        cuts.reverse()
        return f[N][m], cuts

    best_diff = INF
    best_sums = None

    for s in range(n):
        b = [A[(s + t) % n] for t in range(n)]
        pre = [0] * (n + 1)
        for i, v in enumerate(b):
            pre[i + 1] = pre[i] + v
        cand_L = set()
        cap = total // N
        for i in range(n):
            for j in range(i + 1, n + 1):
                v = pre[j] - pre[i]
                if v <= cap:
                    cand_L.add(v)
        cand_L.add(0)
        for L in sorted(cand_L, reverse=True):
            res = solve_linear(b, L)
            if res is None:
                continue
            mx, cuts = res
            sums = [pre[e] - pre[st] for st, e in cuts]
            diff = max(sums) - min(sums)
            if diff < best_diff:
                best_diff = diff
                # rotate so that the part holding original index 0 comes first
                zero_pos = (n - s) % n
                start_idx = 0
                for idx, (st, e) in enumerate(cuts):
                    if st <= zero_pos < e:
                        start_idx = idx
                        break
                best_sums = sums[start_idx:] + sums[:start_idx]
            if best_diff == 0:
                break
        if best_diff == 0:
            break

    return best_sums if best_sums is not None else []
