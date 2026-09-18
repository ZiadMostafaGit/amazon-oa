# Counting: an alternating arrangement fixes the parity pattern, so multiply the two factorials.
from math import factorial


def countGoodPermutations(n: int) -> int:
    odds = (n + 1) // 2
    evens = n // 2
    if odds == evens:
        return 2 * factorial(odds) * factorial(evens)
    if odds == evens + 1:
        return factorial(odds) * factorial(evens)
    return 0
