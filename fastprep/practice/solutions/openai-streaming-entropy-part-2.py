# Max-shifted softmax: H = log(sumExp) - sum(e_i*(x_i - m))/sumExp, computed from shifted logits only.
import math
from typing import List, Optional, Any


def stableEntropy(logits: List[float]) -> float:
    m = max(logits)
    total = 0.0
    weighted = 0.0
    for x in logits:
        d = x - m
        e = math.exp(d) if d > -745.0 else 0.0
        total += e
        weighted += e * d
    if total <= 0.0:
        return 0.0
    h = math.log(total) - weighted / total
    if not (h > 0.0):
        return 0.0
    return h
