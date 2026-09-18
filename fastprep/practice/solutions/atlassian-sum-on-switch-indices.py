# Coordinate-compressed difference array: sum arithmetic series over odd-parity segments.
from typing import List, Optional, Any


def sumOnSwitchIndices(operations: List[List[int]]) -> int:
    delta = {}
    for left, right in operations:
        delta[left] = delta.get(left, 0) + 1
        delta[right + 1] = delta.get(right + 1, 0) - 1

    points = sorted(delta)
    total = 0
    parity = 0
    for i, p in enumerate(points):
        parity += delta[p]
        if parity % 2 == 1 and i + 1 < len(points):
            a = p
            b = points[i + 1] - 1      # inclusive end of this segment
            if b >= a:
                total += (a + b) * (b - a + 1) // 2
    return total
