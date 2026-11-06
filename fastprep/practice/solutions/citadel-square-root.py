# Bisection over the reals: the root lies in [0, max(1, x)]; halve the bracket a fixed number of times.
from typing import List, Optional, Any


def squareRoot(x: float) -> float:
    if x == 0:
        return 0.0
    lo, hi = 0.0, max(1.0, x)
    for _ in range(100):
        mid = (lo + hi) / 2
        if mid * mid < x:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2
