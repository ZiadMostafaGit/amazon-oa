# Sort distinct x knots, collapse duplicates to (min y, max y), then binary search the bracketing segment.
from typing import List, Optional, Any
import bisect


def linear_interpolate(n: int, x_knots: List[float], y_knots: List[float], x_input: float) -> float:
    agg = {}
    m = min(len(x_knots), len(y_knots))
    for i in range(m):
        x = x_knots[i]
        y = y_knots[i]
        cur = agg.get(x)
        if cur is None:
            agg[x] = [y, y]
        else:
            if y < cur[0]:
                cur[0] = y
            if y > cur[1]:
                cur[1] = y

    xs = sorted(agg)
    k = len(xs)
    if k == 0:
        return 0.0
    if k == 1:
        lo, hi = agg[xs[0]]
        return float(lo if x_input <= xs[0] else hi)

    # Exact hit on a knot: x_input <= x, so the smallest y at that x wins.
    if x_input in agg:
        return float(agg[x_input][0])

    # index of the last knot strictly less than x_input
    i = bisect.bisect_left(xs, x_input) - 1

    if i < 0:
        # extrapolate left: both knots lie to the right of x_input -> smallest y
        x0, x1 = xs[0], xs[1]
        y0, y1 = agg[x0][0], agg[x1][0]
    elif i >= k - 1:
        # extrapolate right: both knots lie to the left of x_input -> largest y
        x0, x1 = xs[k - 2], xs[k - 1]
        y0, y1 = agg[x0][1], agg[x1][1]
    else:
        x0, x1 = xs[i], xs[i + 1]
        y0 = agg[x0][1]   # knot is left of x_input
        y1 = agg[x1][0]   # knot is right of x_input

    return float(y0 + (x_input - x0) * (y1 - y0) / (x1 - x0))
