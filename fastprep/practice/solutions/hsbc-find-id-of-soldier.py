# Each action reverses a disjoint segment; map the queried position back through the one segment containing it.
from typing import List, Optional, Any


def findIdOfSoldier(num: int, actions: int, numSoldiers: int, swaps: List[List[int]], posSoldier: int) -> int:
    for pair in swaps:
        if not pair:
            continue
        left = pair[0]
        right = pair[1] if len(pair) > 1 else pair[0]
        if left > right:
            left, right = right, left
        if left <= posSoldier <= right:
            # Reversal of [left, right] maps position p to left + right - p.
            return left + right - posSoldier
    return posSoldier
