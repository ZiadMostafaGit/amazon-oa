# Approach: digit DP counting values with distinct digits in [0, x], answered as f(right) - f(left - 1).
from functools import lru_cache


def _count_up_to(x: int) -> int:
    if x < 0:
        return 0
    s = str(x)
    n = len(s)

    @lru_cache(maxsize=None)
    def go(i: int, mask: int, tight: bool, started: bool) -> int:
        if i == n:
            return 1 if started else 0
        total = 0
        hi = int(s[i]) if tight else 9
        for d in range(hi + 1):
            nxt_tight = tight and d == hi
            if not started and d == 0:
                total += go(i + 1, 0, nxt_tight, False)
            else:
                bit = 1 << d
                if mask & bit:
                    continue
                total += go(i + 1, mask | bit, nxt_tight, True)
        return total

    result = go(0, 0, True, False) + 1  # +1 counts the value 0 itself
    go.cache_clear()
    return result


def countLoveNumbers(left: int, right: int) -> int:
    return _count_up_to(right) - _count_up_to(left - 1)
