# Single pass softmax entropy via H = logsumexp(x) - sum(p_i * x_i), with a max shift for stability.
import math
from typing import List, Optional, Any


def entropy(logits: List[float]) -> float:
    m = max(logits)
    total = 0.0
    weighted = 0.0
    for x in logits:
        e = math.exp(x - m)
        total += e
        weighted += e * (x - m)
    if total == 0.0:
        return 0.0
    h = math.log(total) - weighted / total
    return h if h > 0.0 else 0.0
