# Maintain a set of live houses; each removal changes the segment count by +1, 0 or -1
# depending on how many of its two integer neighbours are still alive.
from typing import List, Optional, Any


def countHouseSegmentsAfterDestruction(houses: List[int], queries: List[int]) -> List[int]:
    alive = set(houses)
    # Initial number of maximal runs of consecutive integers.
    segments = 0
    for h in alive:
        if h - 1 not in alive:
            segments += 1

    result: List[int] = []
    for q in queries:
        if q in alive:
            alive.discard(q)
            left = (q - 1) in alive
            right = (q + 1) in alive
            if left and right:
                segments += 1
            elif not left and not right:
                segments -= 1
        result.append(segments)
    return result
