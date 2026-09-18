# Mark adjacent-differing positions on the circle, then sliding-window count of runs of size-1 marks.
from typing import List, Optional, Any


def solution(tileColors: List[int], size: int) -> int:
    n = len(tileColors)
    if size <= 1:
        return n
    diff = [1 if tileColors[i] != tileColors[(i + 1) % n] else 0 for i in range(n)]
    need = size - 1
    if need >= n:
        # every circular window of length need covers all marks (possibly repeated)
        return n if all(diff) else 0
    window = sum(diff[:need])
    count = 1 if window == need else 0
    for start in range(1, n):
        window -= diff[start - 1]
        window += diff[(start + need - 1) % n]
        if window == need:
            count += 1
    return count
