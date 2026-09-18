# Linear DP over cells, relaxing from step 1 and from every prime jump ending in digit 3.
from typing import List, Optional, Any


def _primes_ending_in_3(limit: int) -> List[int]:
    if limit < 3:
        return []
    sieve = bytearray([1]) * (limit + 1)
    sieve[0:2] = b"\x00\x00"
    i = 2
    while i * i <= limit:
        if sieve[i]:
            sieve[i * i:limit + 1:i] = bytearray(len(range(i * i, limit + 1, i)))
        i += 1
    return [p for p in range(3, limit + 1) if sieve[p] and p % 10 == 3]


def maximumScore(cell: List[int]) -> int:
    n = len(cell)
    if n == 0:
        return 0
    NEG = float("-inf")
    jumps = _primes_ending_in_3(n - 1)
    dp = [NEG] * n
    dp[0] = cell[0]
    for i in range(1, n):
        best = dp[i - 1]
        for p in jumps:
            if p > i:
                break
            prev = dp[i - p]
            if prev > best:
                best = prev
        if best != NEG:
            dp[i] = best + cell[i]
    return dp[n - 1] if dp[n - 1] != NEG else 0
