# The interior sums cancel, so the score is values[i] + values[j]: take the two largest values.
from typing import List, Optional, Any


def maximumEndpointSum(values: List[int]) -> int:
    best = None
    second = None
    for x in values:
        if best is None or x > best:
            second = best
            best = x
        elif second is None or x > second:
            second = x
    return best + second
