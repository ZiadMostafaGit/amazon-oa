# For each anchor point, bucket the other points by normalized slope (reduced dx/dy).
from typing import List, Optional, Any
from math import gcd


def maxPointsOnLine(points: List[List[int]]) -> int:
    n = len(points)
    if n <= 2:
        return n
    best = 2
    for i in range(n):
        x1, y1 = points[i][0], points[i][1]
        slopes = {}
        for j in range(i + 1, n):
            dx = points[j][0] - x1
            dy = points[j][1] - y1
            g = gcd(abs(dx), abs(dy))
            if g:
                dx //= g
                dy //= g
            if dx < 0 or (dx == 0 and dy < 0):
                dx = -dx
                dy = -dy
            key = (dx, dy)
            c = slopes.get(key, 0) + 1
            slopes[key] = c
            if c + 1 > best:
                best = c + 1
    return best
