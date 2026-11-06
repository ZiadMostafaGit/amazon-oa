# Sieve of Eratosthenes: cross out multiples of each prime p starting from p*p.
from typing import List


def primesLessThan(n: int) -> List[int]:
    if n < 3:
        return []
    is_p = bytearray([1]) * n
    is_p[0] = is_p[1] = 0
    p = 2
    while p * p < n:
        if is_p[p]:
            is_p[p * p::p] = bytes(len(range(p * p, n, p)))
        p += 1
    return [i for i in range(n) if is_p[i]]
