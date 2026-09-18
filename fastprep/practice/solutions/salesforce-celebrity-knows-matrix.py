# Two-pointer candidate elimination in O(n), then a single O(n) verification pass.
from typing import List, Optional, Any


def findCelebrity(knows: List[List[int]]) -> int:
    n = len(knows)
    if n == 0:
        return -1
    candidate = 0
    for i in range(1, n):
        if knows[candidate][i]:
            candidate = i
    for i in range(n):
        if i == candidate:
            continue
        if knows[candidate][i] or not knows[i][candidate]:
            return -1
    return candidate
