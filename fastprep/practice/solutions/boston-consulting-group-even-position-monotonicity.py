# Collect even-index values and test strict monotonicity in one pass.
from typing import List, Optional, Any


def solution(numbers: List[int]) -> str:
    vals = numbers[0::2]
    inc = all(vals[i] < vals[i + 1] for i in range(len(vals) - 1))
    dec = all(vals[i] > vals[i + 1] for i in range(len(vals) - 1))
    if inc and not dec:
        return "increasing"
    if dec and not inc:
        return "decreasing"
    return "none"
