# Sieve smallest-prime-factor, accumulate flip parity per prime, then flip multiples once per odd prime.
from typing import List, Optional, Any


def lightBulbs(states: List[int], numbers: List[int]) -> List[int]:
    n = len(states)
    res = list(states)
    if not numbers:
        return res
    limit = max(numbers)
    spf = list(range(limit + 1))
    i = 2
    while i * i <= limit:
        if spf[i] == i:
            for j in range(i * i, limit + 1, i):
                if spf[j] == j:
                    spf[j] = i
        i += 1
    parity = {}
    for v in numbers:
        while v > 1:
            p = spf[v]
            parity[p] = parity.get(p, 0) ^ 1
            while v % p == 0:
                v //= p
    for p, odd in parity.items():
        if odd and p <= n:
            for pos in range(p, n + 1, p):
                res[pos - 1] ^= 1
    return res
