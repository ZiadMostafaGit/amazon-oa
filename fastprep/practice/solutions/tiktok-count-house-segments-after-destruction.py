# Maintain a live set of houses; each removal shifts the segment count by its neighbor occupancy.
from typing import List, Optional, Any


def countHouseSegmentsAfterDestruction(houses: List[int], queries: List[int]) -> List[int]:
    live = set(houses)
    # initial number of maximal runs: one per house with no house immediately before it
    segments = 0
    for h in live:
        if h - 1 not in live:
            segments += 1

    out: List[int] = []
    for q in queries:
        if q in live:
            live.discard(q)
            left = (q - 1) in live
            right = (q + 1) in live
            if left and right:
                segments += 1
            elif not left and not right:
                segments -= 1
        out.append(segments)
    return out
