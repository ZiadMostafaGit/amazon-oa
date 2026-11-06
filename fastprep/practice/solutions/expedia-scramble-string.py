# Interval DP over (start in first, start in second, length): try every split, kept or swapped.
from functools import lru_cache


def isScramble(first: str, second: str) -> bool:
    if len(first) != len(second):
        return False

    @lru_cache(maxsize=None)
    def go(i, j, n):
        a, b = first[i:i + n], second[j:j + n]
        if a == b:
            return True
        if sorted(a) != sorted(b):
            return False
        for k in range(1, n):
            if go(i, j, k) and go(i + k, j + k, n - k):
                return True
            if go(i, j + n - k, k) and go(i + k, j, n - k):
                return True
        return False

    return go(0, 0, len(first))
