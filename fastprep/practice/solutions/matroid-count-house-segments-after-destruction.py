# Hash-set simulation: removing a house splits, shrinks, or deletes a segment based on its two neighbours.
from typing import List, Optional, Any


def solution(houses: List[int], queries: List[int]) -> List[int]:
    alive = set(houses)
    # initial segment count: a house starts a segment when pos-1 is absent
    count = sum(1 for p in alive if (p - 1) not in alive)

    res = []
    for q in queries:
        if q in alive:
            left = (q - 1) in alive
            right = (q + 1) in alive
            alive.discard(q)
            if left and right:
                count += 1
            elif not left and not right:
                count -= 1
        res.append(count)
    return res
