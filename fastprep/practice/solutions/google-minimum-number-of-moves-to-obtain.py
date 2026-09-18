# Sum of positive rises in the array (each rise starts that many new intervals).
from typing import List


def solve(A: List[int]) -> int:
    total = 0
    prev = 0
    for v in A:
        if v > prev:
            total += v - prev
        prev = v
    return total
