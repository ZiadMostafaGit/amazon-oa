# Counting: for every candidate package cost S, singles of cost S plus greedy pair matches (a, S-a).
from typing import List, Optional, Any


def maximumNumberOfPackages(n: int, cost: List[int]) -> int:
    MAXV = 2000
    cnt = [0] * (MAXV + 1)
    for c in cost:
        cnt[c] += 1

    best = 0
    for s in range(1, 2 * MAXV + 1):
        total = cnt[s] if s <= MAXV else 0
        a = 1
        b = s - 1
        while a < b:
            if b <= MAXV:
                total += min(cnt[a], cnt[b])
            a += 1
            b -= 1
        if a == b and a <= MAXV:
            total += cnt[a] // 2
        if total > best:
            best = total
    return best
