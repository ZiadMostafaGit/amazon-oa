# Greedy: keep each room's busy-until time, assign the lowest-numbered room free at the request start.
from typing import List, Optional, Any


def solve(roomCount: int, meetings: List[List[int]]) -> List[int]:
    free_at = [float('-inf')] * roomCount
    res = []
    for start, end in meetings:
        chosen = -1
        for r in range(roomCount):
            if free_at[r] <= start:
                chosen = r
                break
        if chosen != -1:
            free_at[chosen] = end
        res.append(chosen)
    return res
