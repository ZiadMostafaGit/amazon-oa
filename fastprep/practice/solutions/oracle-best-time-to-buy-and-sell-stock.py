# Single pass tracking the minimum price seen so far.
from typing import List, Optional, Any


def maxProfit(prices: List[int]) -> int:
    best = 0
    lo = None
    for p in prices:
        if lo is None or p < lo:
            lo = p
        elif p - lo > best:
            best = p - lo
    return best
