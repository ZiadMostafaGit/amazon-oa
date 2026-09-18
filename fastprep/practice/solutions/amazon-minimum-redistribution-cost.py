# One-directional circular flow: cost = sum(prefix deltas) - n*min(prefix), taken over both orientations.
from typing import List, Optional, Any


def getMinimumRedistributionCost(products: List[int]) -> int:
    n = len(products)
    avg = sum(products) // n

    def directional(arr):
        total = 0
        running = 0
        lowest = 0
        for v in arr:
            running += v - avg
            total += running
            if running < lowest:
                lowest = running
        return total - n * lowest

    return min(directional(products), directional(products[::-1]))
