# Greedy: the n-1 largest packets become singleton channels, the rest form one channel (its median).
from typing import List, Optional, Any


def calculateMedianSum(packets: List[int], n: int) -> int:
    a = sorted(packets)
    m = len(a)
    if n <= 0 or m == 0:
        return 0
    if n >= m:
        return sum(a)
    # twice the total, to keep the .5 from an even-sized median exact
    twice = 2 * sum(a[m - (n - 1):]) if n > 1 else 0
    rest = a[: m - (n - 1)]
    k = len(rest)
    if k % 2 == 1:
        twice += 2 * rest[k // 2]
    else:
        twice += rest[k // 2 - 1] + rest[k // 2]
    # round half away from zero
    if twice >= 0:
        return (twice + 1) // 2
    return -((-twice + 1) // 2)
