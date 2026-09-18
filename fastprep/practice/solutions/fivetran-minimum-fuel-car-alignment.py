# Separable Manhattan cost: median row for y, and median of sorted x minus index for the run of x slots.
from typing import List, Optional, Any


def minimumFuelCost(xCoordinates: List[int], yCoordinates: List[int]) -> int:
    n = len(xCoordinates)
    if n == 0:
        return 0

    ys = sorted(yCoordinates)
    row = ys[n // 2]
    cost = sum(abs(y - row) for y in ys)

    xs = sorted(xCoordinates)
    shifted = [xs[i] - i for i in range(n)]
    shifted.sort()
    start = shifted[n // 2]
    cost += sum(abs(v - start) for v in shifted)
    return cost
