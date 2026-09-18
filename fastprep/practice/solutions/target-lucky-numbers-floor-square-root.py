# Closed-form counting: each k contributes k^2, k^2+k, k^2+2k, so count(N) is O(1) via isqrt; answer = f(r) - f(l-1).
from math import isqrt


def _count_up_to(n: int) -> int:
    if n < 1:
        return 0
    k = isqrt(n)
    # every k' < k contributes exactly 3 lucky numbers; the last block may be partial
    return 3 * (k - 1) + min(3, (n - k * k) // k + 1)


def countLuckyNumbers(l: int, r: int) -> int:
    return _count_up_to(r) - _count_up_to(l - 1)
