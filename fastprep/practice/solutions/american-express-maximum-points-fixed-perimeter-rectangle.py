# Enumerate candidate left/right x boundaries, then slide a height window over sorted y values.
from typing import List, Optional, Any


def maxPointsWithPerimeter(points: List[List[int]], perimeter: int) -> int:
    xs = sorted({p[0] for p in points})
    pts = sorted(points, key=lambda p: p[0])
    best = 0
    for i, x1 in enumerate(xs):
        for x2 in xs[i:]:
            width = x2 - x1
            if 2 * width > perimeter:
                break
            max_height = (perimeter - 2 * width) // 2
            ys = sorted(p[1] for p in pts if x1 <= p[0] <= x2)
            left = 0
            for right in range(len(ys)):
                while ys[right] - ys[left] > max_height:
                    left += 1
                span = right - left + 1
                if span > best:
                    best = span
    return best
