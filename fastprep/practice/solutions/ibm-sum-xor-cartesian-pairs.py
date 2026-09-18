# Bitwise counting: for each bit, pairs contribute 2^b times (ones on one side * zeros on the other).
from typing import List, Optional, Any


def sumPairXor(left: List[int], right: List[int]) -> int:
    n, m = len(left), len(right)
    total = 0
    for b in range(31):
        mask = 1 << b
        ones_l = sum(1 for v in left if v & mask)
        ones_r = sum(1 for v in right if v & mask)
        differing = ones_l * (m - ones_r) + (n - ones_l) * ones_r
        total += differing * mask
    return total
