# Single pass tracking the minimum price seen so far and the best profit against it.
from typing import List, Optional, Any


def maxProfit(prices: List[int]) -> int:
    best = 0
    low = None
    for p in prices:
        if low is None or p < low:
            low = p
        elif p - low > best:
            best = p - low
    return best
