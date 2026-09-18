# Chain rule: sort permutation routes v/m back to each input, plus the median's denominator term.
from typing import List, Optional, Any


def backpropSortMedian(x: List[float], v: List[float]) -> List[float]:
    n = len(x)
    if n == 0:
        return []
    order = sorted(range(n), key=lambda i: x[i])
    mid = n // 2
    m = float(x[order[mid]])
    grad = [0.0] * n
    for pos, i in enumerate(order):
        grad[i] = v[pos] / m
    # d/dm of (s_k / m) = -s_k / m^2, summed over all outputs
    total = 0.0
    for pos, i in enumerate(order):
        total += v[pos] * float(x[i])
    grad[order[mid]] += -total / (m * m)
    return grad
