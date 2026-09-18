# Merge each pin's intervals, then sweep a difference array over all event timestamps.
from typing import List, Optional, Any


def uniqueActivePinTimeline(logs: List[List[int]]) -> List[List[int]]:
    if not logs:
        return []

    by_pin = {}
    stamps = set()
    for pin, s, e in logs:
        stamps.add(s)
        stamps.add(e)
        by_pin.setdefault(pin, []).append((s, e))

    delta = {}
    for intervals in by_pin.values():
        intervals.sort()
        cs, ce = intervals[0]
        for s, e in intervals[1:]:
            if s <= ce:
                if e > ce:
                    ce = e
            else:
                delta[cs] = delta.get(cs, 0) + 1
                delta[ce] = delta.get(ce, 0) - 1
                cs, ce = s, e
        delta[cs] = delta.get(cs, 0) + 1
        delta[ce] = delta.get(ce, 0) - 1

    ts = sorted(stamps)
    out = []
    cur = 0
    for i in range(len(ts) - 1):
        cur += delta.get(ts[i], 0)
        out.append([ts[i], ts[i + 1], cur])
    return out
