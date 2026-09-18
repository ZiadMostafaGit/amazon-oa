# Bitmask DP over visited currencies (n <= 8): best multiplier per (visited set, node), memoized per source.
from typing import List, Optional, Any


def maximumConversions(currencyCount: int, edges: List[List[int]], rates: List[float], queries: List[List[int]], amounts: List[float]) -> List[float]:
    adj = [[] for _ in range(currencyCount)]
    for (u, v), r in zip(edges, rates):
        adj[u].append((v, float(r)))

    cache = {}

    def best_from(src: int) -> List[float]:
        if src in cache:
            return cache[src]
        full = 1 << currencyCount
        NEG = float('-inf')
        dp = [[NEG] * currencyCount for _ in range(full)]
        dp[1 << src][src] = 1.0
        for mask in range(full):
            row = dp[mask]
            for u in range(currencyCount):
                cur = row[u]
                if cur == NEG:
                    continue
                for v, r in adj[u]:
                    bit = 1 << v
                    if mask & bit:
                        continue
                    nm = mask | bit
                    val = cur * r
                    if val > dp[nm][v]:
                        dp[nm][v] = val
        res = [NEG] * currencyCount
        for mask in range(full):
            row = dp[mask]
            for v in range(currencyCount):
                if row[v] > res[v]:
                    res[v] = row[v]
        cache[src] = res
        return res

    out = []
    for (s, t), amt in zip(queries, amounts):
        if s == t:
            out.append(float(amt))
            continue
        m = best_from(s)[t]
        out.append(-1.0 if m == float('-inf') else float(amt) * m)
    return out
