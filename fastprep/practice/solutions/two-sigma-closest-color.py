# Brute force: parse 8-bit RGB components, compare squared distance to the five pure colors.
from typing import List, Optional, Any

PURE = [
    ("Black", (0, 0, 0)),
    ("White", (255, 255, 255)),
    ("Red", (255, 0, 0)),
    ("Green", (0, 255, 0)),
    ("Blue", (0, 0, 255)),
]


def closestColor(pixels: List[str]) -> List[str]:
    out = []
    for p in pixels:
        s = p.strip()
        r = int(s[0:8], 2)
        g = int(s[8:16], 2)
        b = int(s[16:24], 2)
        best = None
        name = None
        tie = False
        for nm, (pr, pg, pb) in PURE:
            d = (r - pr) ** 2 + (g - pg) ** 2 + (b - pb) ** 2
            if best is None or d < best:
                best = d
                name = nm
                tie = False
            elif d == best:
                tie = True
        out.append("Ambiguous" if tie else name)
    return out
