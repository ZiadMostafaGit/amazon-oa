# Top-two scan: winner i ties or beats every rival's best case iff r[i] + 1 >= max of the others.
from typing import List, Optional, Any


def countPossibleWinners(initialRewards: List[int], n: int) -> int:
    if n <= 1:
        return len(initialRewards)
    best = second = None
    for v in initialRewards:
        if best is None or v > best:
            second = best
            best = v
        elif second is None or v > second:
            second = v
    count = 0
    seen_best = False
    for v in initialRewards:
        if v == best and not seen_best:
            seen_best = True
            other = second
        else:
            other = best
        if v + 1 >= other:
            count += 1
    return count
