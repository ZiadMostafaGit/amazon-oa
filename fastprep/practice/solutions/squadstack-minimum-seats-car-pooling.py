# Sweep line over delta events sorted by position (drop-offs applied before pickups).
from typing import List, Optional, Any


def minimumSeats(stops: List[List[int]]) -> int:
    events = []
    for passengers, start, end in stops:
        events.append((start, passengers))
        events.append((end, -passengers))
    # sorting by (point, delta) puts negative deltas (drop-offs) first at a shared point
    events.sort()
    onboard = 0
    best = 0
    for _, delta in events:
        onboard += delta
        if onboard > best:
            best = onboard
    return best
