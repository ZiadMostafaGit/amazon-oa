# Approach: equal-mass elastic collisions are equivalent to trucks passing through each other, so the
# multiset of exit times equals the free-motion exit times; answer is their maximum (-1 if some truck never exits).
from typing import List, Optional, Any


def lastTruckExitTime(laneLength: int, initial: List[int], velocity: List[int]) -> float:
    last = 0.0
    for x, v in zip(initial, velocity):
        if v > 0:
            t = (laneLength - x) / float(v)
        elif v < 0:
            t = x / float(-v)
        else:
            # a stationary trajectory always survives, so no truck ever finishes leaving
            return -1.0
        if t > last:
            last = t
    return float(last)
