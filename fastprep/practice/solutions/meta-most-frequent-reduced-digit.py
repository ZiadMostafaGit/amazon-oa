from typing import List, Optional, Any


def solution(readings: List[int]) -> int:
    count = [0] * 10
    for x in readings:
        while x >= 10:
            x = sum(int(d) for d in str(x))
        count[x] += 1
    best = 0
    for d in range(10):
        if count[d] >= count[best] and count[d] > 0:
            best = d
    return best
