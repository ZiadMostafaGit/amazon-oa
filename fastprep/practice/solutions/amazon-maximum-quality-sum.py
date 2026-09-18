# Greedy: sort descending, give the top channels-1 packets their own channel, rest share one; median via doubled arithmetic.
from typing import List, Optional, Any


def maximumQualitySum(packets: List[int], channels: int) -> int:
    arr = sorted(packets, reverse=True)
    k = channels - 1
    doubled = 2 * sum(arr[:k])
    rest = arr[k:]
    m = len(rest)
    # rest is sorted descending; median is same regardless of direction
    if m % 2 == 1:
        doubled += 2 * rest[m // 2]
    else:
        doubled += rest[m // 2 - 1] + rest[m // 2]
    return (doubled + 1) // 2
