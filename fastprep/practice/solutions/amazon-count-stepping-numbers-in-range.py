# Digit DP over decimal strings: count(high) - count(low-1).
from functools import lru_cache


def _count_upto(n: int) -> int:
    if n < 0:
        return 0
    s = str(n)
    L = len(s)

    @lru_cache(maxsize=None)
    def dp(pos: int, prev: int, tight: bool, started: bool) -> int:
        if pos == L:
            return 1 if started else 0
        limit = int(s[pos]) if tight else 9
        total = 0
        for d in range(0, limit + 1):
            if not started:
                if d == 0:
                    total += dp(pos + 1, -1, tight and d == limit, False)
                else:
                    total += dp(pos + 1, d, tight and d == limit, True)
            else:
                if abs(d - prev) == 1:
                    total += dp(pos + 1, d, tight and d == limit, True)
        return total

    res = dp(0, -1, True, False) + 1  # +1 counts the number 0 itself
    dp.cache_clear()
    return res


def solve(low: int, high: int) -> int:
    return _count_upto(high) - _count_upto(low - 1)
