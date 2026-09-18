# DP over indices: dp[i] = arr[i] + max(dp[i-1], dp[i-p]) for sieved primes p ending in digit 3.
from typing import List, Optional, Any


def _primes_ending_in_three(limit: int) -> List[int]:
    # limit is inclusive; returns primes p <= limit with p % 10 == 3.
    if limit < 3:
        return []
    sieve = bytearray([1]) * (limit + 1)
    sieve[0] = 0
    if limit >= 1:
        sieve[1] = 0
    i = 2
    while i * i <= limit:
        if sieve[i]:
            sieve[i * i::i] = bytearray(len(sieve[i * i::i]))
        i += 1
    return [p for p in range(3, limit + 1, 10) if sieve[p]]


def maxJumpScore(arr: List[int]) -> int:
    n = len(arr)
    if n <= 1:
        return arr[0] if n == 1 else 0
    primes = _primes_ending_in_three(n - 1)
    dp = [0] * n
    dp[0] = arr[0]
    for i in range(1, n):
        best = dp[i - 1]
        for p in primes:
            if p > i:
                break
            v = dp[i - p]
            if v > best:
                best = v
        dp[i] = best + arr[i]
    return dp[n - 1]
