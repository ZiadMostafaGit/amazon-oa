# Direct simulation: subtract each number from the larger of x and y, else count it as skipped.
from typing import List, Optional, Any


def solution(x: int, y: int, numbers: List[int]) -> int:
    skipped = 0
    for n in numbers:
        if n > x and n > y:
            skipped += 1
        elif x >= y:
            x -= n
        else:
            y -= n
    return skipped
