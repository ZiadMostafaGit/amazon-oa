# Approach: flatten to a hash set, then count each unordered complement pair once (values are globally unique).
from typing import List


def solve(matrix: List[List[int]], target: int) -> int:
    seen = set()
    for row in matrix:
        for v in row:
            seen.add(v)
    count = 0
    for v in seen:
        c = target - v
        if c in seen and v < c:
            count += 1
    return count
