# Approach: per-digit positional counting (digit DP formula) for each of the digits 0, 2 and 4.
def _count_digit(n: int, d: int) -> int:
    # occurrences of digit d in the decimal representations of 1..n
    if n <= 0:
        return 0
    total = 0
    p = 1
    while p <= n:
        high = n // (p * 10)
        cur = (n // p) % 10
        low = n % p
        if d > 0:
            total += high * p
            if cur > d:
                total += p
            elif cur == d:
                total += low + 1
        else:
            total += (high - 1) * p
            if cur > 0:
                total += p
            else:
                total += low + 1
        p *= 10
    return total


def solution(n: int) -> int:
    if n < 0:
        return 0
    # the number 0 itself contributes a single digit 0
    return 1 + sum(_count_digit(n, d) for d in (0, 2, 4))
