# Coordinate sweep: split the timeline at every start/end boundary and list the people covering each slice.
from typing import List


def solve(roster: List[List[str]]) -> List[List[str]]:
    if not roster:
        return []

    entries = []
    bounds = set()
    for idx, row in enumerate(roster):
        name = row[0]
        start = int(row[1])
        end = int(row[2])
        if start >= end:
            continue
        entries.append((start, end, idx, name))
        bounds.add(start)
        bounds.add(end)

    if not entries:
        return []

    points = sorted(bounds)
    starts = sorted(entries, key=lambda e: e[0])

    result = []
    active = []  # (order index, name, end)
    ptr = 0
    n = len(starts)
    for i in range(len(points) - 1):
        lo = points[i]
        hi = points[i + 1]
        while ptr < n and starts[ptr][0] <= lo:
            s, e, idx, name = starts[ptr]
            active.append((idx, name, e))
            ptr += 1
        active = [p for p in active if p[2] > lo]
        active.sort(key=lambda p: p[0])
        names = ",".join(p[1] for p in active)
        result.append([str(lo), str(hi), names])

    return result
