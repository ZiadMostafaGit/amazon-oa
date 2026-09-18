# Running accumulation of sum(x*y) and sum(x^2), emitting the slope after each batch.
from typing import List, Optional, Any


def onlineNoInterceptSlopes(xBatches: List[List[float]], yBatches: List[List[float]]) -> List[float]:
    numerator = 0.0
    denominator = 0.0
    out: List[float] = []
    for xs, ys in zip(xBatches, yBatches):
        for x, y in zip(xs, ys):
            numerator += x * y
            denominator += x * x
        out.append(numerator / denominator)
    return out
