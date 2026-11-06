# Every item weighs 1, so any item can replace any other: take the most valuable items first.
# A capacity-indexed DP is impossible (capacity and copies up to 10^9) and unnecessary.
from typing import List


def maxValue(values: List[int], quantities: List[int], capacity: int) -> int:
    total = 0
    for v, q in sorted(zip(values, quantities), reverse=True):
        if capacity == 0:
            break
        take = min(q, capacity)
        total += take * v
        capacity -= take
    return total
