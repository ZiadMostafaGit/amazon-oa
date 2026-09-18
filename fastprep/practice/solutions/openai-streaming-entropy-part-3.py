# Streaming aggregates: keep S = sum(exp(x)) and T = sum(x*exp(x)); H = ln(S) - T/S.
from typing import List, Optional, Any
import math


def blockwiseEntropy(blocks: List[List[float]]) -> float:
    s = 0.0   # sum of exp(x)
    t = 0.0   # sum of x * exp(x)
    for block in blocks:
        for x in block:
            e = math.exp(x)
            s += e
            t += x * e
    if s == 0.0:
        return 0.0
    h = math.log(s) - t / s
    if h < 0.0:
        h = 0.0
    return h
