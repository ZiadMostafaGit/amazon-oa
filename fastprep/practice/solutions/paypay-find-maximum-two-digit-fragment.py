# Sliding window of width 2 over the digit string, tracking the max integer value.
from typing import List, Optional, Any


def solution(S: str) -> int:
    best = -1
    for i in range(len(S) - 1):
        v = int(S[i:i + 2])
        if v > best:
            best = v
    return best
