# Greedy: watch whichever category finishes earliest first, then the best second movie; try both orders.
from typing import List, Optional, Any


def minimumTimeSpent(comedyReleaseTime: List[int], comedyDuration: List[int], dramaReleaseTime: List[int], dramaDuration: List[int]) -> int:
    def best(firstRel, firstDur, secondRel, secondDur):
        # earliest possible finish of the first movie
        t = min(r + d for r, d in zip(firstRel, firstDur))
        # then the second movie, started as soon as it is available
        return min(max(t, r) + d for r, d in zip(secondRel, secondDur))

    return min(
        best(comedyReleaseTime, comedyDuration, dramaReleaseTime, dramaDuration),
        best(dramaReleaseTime, dramaDuration, comedyReleaseTime, comedyDuration),
    )
