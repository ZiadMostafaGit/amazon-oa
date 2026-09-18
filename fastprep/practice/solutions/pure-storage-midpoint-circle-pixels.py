# Midpoint (Bresenham) circle algorithm with 8-way symmetry, deduplicated and sorted by (x, y).
from typing import List, Optional, Any


def drawCirclePixels(radius: int) -> List[List[int]]:
    pixels = set()
    x, y = 0, radius
    d = 1 - radius
    while x <= y:
        for px, py in ((x, y), (x, -y), (-x, y), (-x, -y),
                       (y, x), (y, -x), (-y, x), (-y, -x)):
            pixels.add((px, py))
        old_d = d
        x += 1
        if old_d < 0:
            d = d + 2 * x + 1
        else:
            y -= 1
            d = d + 2 * (x - y) + 1
    return [[px, py] for px, py in sorted(pixels)]
