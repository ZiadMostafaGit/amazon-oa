# Backtracking over value-count multiset with memoization: always fix the smallest remaining value.
from typing import List, Optional, Any
from functools import lru_cache


def canPartitionIntoFifteens(cards: List[int]) -> bool:
    n = len(cards)
    if n % 3 != 0:
        return False
    if n == 0:
        return True
    if sum(cards) != 15 * (n // 3):
        return False

    counts = [0] * 10
    for v in cards:
        counts[v] += 1

    @lru_cache(maxsize=None)
    def solve(state: tuple) -> bool:
        cnt = list(state)
        a = -1
        for v in range(1, 10):
            if cnt[v] > 0:
                a = v
                break
        if a == -1:
            return True
        cnt[a] -= 1
        rest = 15 - a
        for b in range(a, 10):
            c = rest - b
            if c < b or c > 9:
                continue
            if b == c:
                if cnt[b] < 2:
                    continue
                cnt[b] -= 2
                ok = solve(tuple(cnt))
                cnt[b] += 2
            else:
                if cnt[b] < 1 or cnt[c] < 1:
                    continue
                cnt[b] -= 1
                cnt[c] -= 1
                ok = solve(tuple(cnt))
                cnt[b] += 1
                cnt[c] += 1
            if ok:
                return True
        return False

    return solve(tuple(counts))
