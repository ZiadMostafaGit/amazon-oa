# Maintain a live-position hash set; each removal changes the segment count by +1/0/-1 based on neighbors.
from typing import List, Optional, Any


def solution(houses: List[int], queries: List[int]) -> List[int]:
    alive = set(houses)
    segments = 0
    for h in alive:
        if (h - 1) not in alive:
            segments += 1
    res = []
    for q in queries:
        alive.discard(q)
        left = (q - 1) in alive
        right = (q + 1) in alive
        if left and right:
            segments += 1
        elif not left and not right:
            segments -= 1
        res.append(segments)
    return res
