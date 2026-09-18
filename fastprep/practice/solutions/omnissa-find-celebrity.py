# Two-pass candidate elimination: one linear scan to find the only possible celebrity, one to verify.
from typing import List, Optional, Any


def findCelebrity(knows: List[List[int]]) -> int:
    n = len(knows)
    if n == 1:
        return 0

    candidate = 0
    for i in range(1, n):
        if knows[candidate][i] == 1:
            candidate = i

    for i in range(n):
        if i == candidate:
            continue
        if knows[candidate][i] == 1 or knows[i][candidate] == 0:
            return -1
    return candidate
