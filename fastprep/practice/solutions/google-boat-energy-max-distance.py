# DP over (day, remaining energy): each day either move (spend 1) or rest (gain 1, capped at k).
from typing import List, Optional, Any


def solve(k: int, wind: List[int]) -> int:
    n = len(wind)
    if n == 0 or k <= 0:
        return 0
    cap = min(k, n)  # energy above n can never be spent
    NEG = float("-inf")
    dp = [NEG] * (cap + 1)
    dp[cap] = 0
    for w in wind:
        nxt = [NEG] * (cap + 1)
        for e in range(cap + 1):
            cur = dp[e]
            if cur == NEG:
                continue
            r = e + 1 if e + 1 <= cap else cap  # rest
            if cur > nxt[r]:
                nxt[r] = cur
            if e > 0:  # move
                v = cur + w
                if v > nxt[e - 1]:
                    nxt[e - 1] = v
        dp = nxt
    best = 0
    for v in dp:
        if v != NEG and v > best:
            best = v
    return best
