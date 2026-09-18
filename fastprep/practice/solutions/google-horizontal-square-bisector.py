# Coordinate-compressed vertical sweep: accumulate area per y-band, then interpolate inside the band that crosses half the total area.
from typing import List


def solve(squares: List[List[int]]) -> float:
    if not squares:
        return 0.0

    intervals = []
    total = 0.0
    for x, top, side in squares:
        bottom = top - side
        intervals.append((bottom, top, float(side)))
        total += float(side) * float(side)

    half = total / 2.0
    if total == 0.0:
        return float(min(iv[0] for iv in intervals))

    # Sweep over compressed y coordinates, tracking the total horizontal width.
    events = []
    for bottom, top, side in intervals:
        events.append((bottom, side))
        events.append((top, -side))
    events.sort(key=lambda e: e[0])

    ys = sorted(set(e[0] for e in events))
    width = 0.0
    acc = 0.0
    idx = 0
    n = len(events)
    for i in range(len(ys) - 1):
        y = ys[i]
        while idx < n and events[idx][0] == y:
            width += events[idx][1]
            idx += 1
        nxt = ys[i + 1]
        span = float(nxt - y)
        band = width * span
        if width > 0.0 and acc + band >= half:
            remaining = half - acc
            return y + remaining / width
        acc += band

    return float(ys[-1])
