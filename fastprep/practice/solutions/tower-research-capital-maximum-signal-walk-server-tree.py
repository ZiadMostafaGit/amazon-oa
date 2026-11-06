from typing import List

MOD = 998244353


def maxSignalWalk(parent: List[int], signals: List[int]) -> int:
    n = len(parent)
    if n == 1:
        s = signals[0]
        return pow(2, abs(s), MOD) if s > 0 else (-pow(2, -s, MOD)) % MOD
    # A walk's visited set is any connected subtree; Y = (+/-) 2^(sum |s|),
    # positive iff the set holds an even number of negative servers.
    children = [[] for _ in range(n)]
    for v in range(1, n):
        children[parent[v]].append(v)
    order = [0]
    for v in order:
        order.extend(children[v])
    NEG = float("-inf")
    # dp[v][p]: best sum of |s| over connected sets whose top is v, parity p.
    dp0 = [NEG] * n
    dp1 = [NEG] * n
    best = NEG
    for v in reversed(order):
        w = abs(signals[v])
        if signals[v] > 0:
            a, b = w, NEG
        else:
            a, b = NEG, w
        for ch in children[v]:
            c0, c1 = dp0[ch], dp1[ch]
            na = max(a, a + c0, b + c1)
            nb = max(b, b + c0, a + c1)
            a, b = na, nb
        dp0[v], dp1[v] = a, b
        if a > best:
            best = a
    return pow(2, int(best), MOD)
