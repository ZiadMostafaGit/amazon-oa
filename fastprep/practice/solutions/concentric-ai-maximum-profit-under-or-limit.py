# For every allowed mask m <= k, take all positive-profit items whose value is a submask of m (SOS-style accumulation).
from typing import List, Optional, Any


def maxProfitUnderOrLimit(values: List[int], profits: List[int], k: int) -> int:
    BITS = 10
    SIZE = 1 << BITS
    # gain[v] = total positive profit of items whose value is exactly v
    gain = [0] * SIZE
    for v, p in zip(values, profits):
        if p > 0 and v < SIZE:
            gain[v] += p
    # subset-sum over subsets: best[m] = sum of gain[s] for every submask s of m
    best = gain[:]
    for b in range(BITS):
        bit = 1 << b
        for m in range(SIZE):
            if m & bit:
                best[m] += best[m ^ bit]
    limit = min(k, SIZE - 1)
    ans = 0
    for m in range(limit + 1):
        if best[m] > ans:
            ans = best[m]
    return ans
