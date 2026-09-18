from typing import List, Optional, Any


def solve(knows: List[List[int]]) -> int:
    n = len(knows) if knows else 0
    if n == 0:
        return -1

    # One linear sweep eliminates n-1 people: if cand knows i, cand is not the
    # celebrity; otherwise i is not (the celebrity is known by everyone).
    cand = 0
    for i in range(1, n):
        if knows[cand][i]:
            cand = i

    for i in range(n):
        if i == cand:
            continue
        if knows[cand][i] or not knows[i][cand]:
            return -1
    return cand
