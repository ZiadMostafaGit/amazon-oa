# Counting check per side: side s fits iff m + 4*min(n, (s//2)^2) >= s*s; scan s up to isqrt(m+4n).
from math import isqrt


def sideLargetstSquare(m: int, n: int) -> int:
    limit = isqrt(m + 4 * n)
    best = 0
    for s in range(1, limit + 1):
        big = min(n, (s // 2) * (s // 2))
        if m + 4 * big >= s * s:
            best = s
    return best
