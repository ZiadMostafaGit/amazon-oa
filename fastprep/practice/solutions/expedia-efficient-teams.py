# Sort and pair the smallest with the largest: the only way every pair reaches the same sum.
from typing import List, Optional, Any


def getTotalEfficiency(skill: List[int]) -> int:
    s = sorted(skill)
    n = len(s)
    target = s[0] + s[-1]
    total = 0
    for i in range(n // 2):
        a, b = s[i], s[n - 1 - i]
        if a + b != target:
            return -1
        total += a * b
    return total
