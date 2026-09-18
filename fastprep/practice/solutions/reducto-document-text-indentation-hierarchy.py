# Approach: exact rational division (scale hundredths to integers) then round the quotient to its nearest integer level.
from typing import List, Optional, Any


def recoverIndentation(texts: List[str], distances: List[List[float]], baseUnit: float) -> List[str]:
    def to_hundredths(x: float) -> int:
        # values have at most two decimals; round away float noise
        return int(round(float(x) * 100))

    base = to_hundredths(baseUnit)
    out = []
    for i, t in enumerate(texts):
        left = to_hundredths(distances[i][0])
        if base <= 0:
            level = 0
        else:
            # nearest integer to left/base without floating point
            level = (2 * left + base) // (2 * base)
        out.append(str(int(level)) + "|" + t)
    return out
