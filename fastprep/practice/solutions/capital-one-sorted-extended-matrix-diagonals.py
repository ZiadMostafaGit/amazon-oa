# Build each of the 2n-1 diagonals, cycle it to length n, then stable-sort the strings by value.
from typing import List, Optional, Any


def solution(matrix: List[List[str]]) -> List[int]:
    n = len(matrix)
    strings = []
    for d in range(1, 2 * n):
        offset = d - n  # cells with c - r == offset
        chars = []
        for r in range(n):
            c = r + offset
            if 0 <= c < n:
                chars.append(matrix[r][c])
        k = len(chars)
        extended = "".join(chars[i % k] for i in range(n))
        strings.append((extended, d))
    strings.sort(key=lambda pair: pair[0])
    return [d for _, d in strings]
