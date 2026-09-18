# One-pass log-sum-exp with a running max: keep S=sum exp(x-m), T=sum (x-m)exp(x-m), rescale on a new max.
from typing import List, Optional, Any
import math


def streamingEntropy(blocks: List[List[float]]) -> float:
    m = -math.inf   # running maximum logit
    s = 0.0         # sum of exp(x - m)
    t = 0.0         # sum of (x - m) * exp(x - m)
    for block in blocks:
        for x in block:
            if x > m:
                if s != 0.0:
                    d = m - x            # negative shift
                    f = math.exp(d)
                    t = (t + d * s) * f
                    s = s * f
                m = x
                s += 1.0                 # exp(x - m) == 1
                # (x - m) * exp(...) == 0, so t is unchanged
            else:
                d = x - m
                e = math.exp(d)
                s += e
                t += d * e
    if s == 0.0:
        return 0.0
    h = math.log(s) - t / s
    if h < 0.0:
        h = 0.0
    return h
