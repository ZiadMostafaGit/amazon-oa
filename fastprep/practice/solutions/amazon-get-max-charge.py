# Parity invariant: any mergeable block holds indices of one parity, so take the best
# positive-only sum within each parity class, falling back to the single largest element.
from typing import List, Optional, Any


def getMaxCharge(charge: List[int]) -> int:
    best = max(charge)
    even_sum = 0
    odd_sum = 0
    for i, value in enumerate(charge):
        if value > 0:
            if i % 2 == 0:
                even_sum += value
            else:
                odd_sum += value
    if even_sum > best:
        best = even_sum
    if odd_sum > best:
        best = odd_sum
    return best
