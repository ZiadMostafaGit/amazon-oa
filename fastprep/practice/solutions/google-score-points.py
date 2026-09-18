# Linear scan: sum token points plus one bonus per adjacent token pair.
from typing import List, Optional, Any


def scorePoints(points: List[int], tokens: str) -> int:
    total = 0
    for i, ch in enumerate(tokens):
        if ch == 'T':
            total += points[i]
            if i > 0 and tokens[i - 1] == 'T':
                total += 1
    return total
