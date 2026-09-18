# Single pass keeping the best departure seen so far, paired with each later return time (O(n)).
from typing import List, Optional, Any


def getMinimumRoundTripCost(departing: List[int], returning: List[int]) -> int:
    n = min(len(departing), len(returning))
    best_depart = None
    best_total = None
    for i in range(n):
        if i > 0:
            if best_depart is not None:
                total = best_depart + returning[i]
                if best_total is None or total < best_total:
                    best_total = total
        d = departing[i]
        if best_depart is None or d < best_depart:
            best_depart = d
    return best_total if best_total is not None else -1
