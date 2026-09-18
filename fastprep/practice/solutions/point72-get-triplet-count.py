# Group values by residue mod d and count 3-subsets by DP over residue classes.
from math import comb
from collections import Counter, defaultdict
from typing import List, Optional, Any


def getTripletCount(arr: List[int], d: int) -> int:
    if d == 0 or len(arr) < 3:
        return 0
    groups = Counter(x % d for x in arr)
    # dp[j][s] = number of ways to pick j items whose residue sum is s (mod d)
    dp = [defaultdict(int) for _ in range(4)]
    dp[0][0] = 1
    for r, m in groups.items():
        ndp = [defaultdict(int, dp[j]) for j in range(4)]
        for t in range(1, 4):
            if m < t:
                break
            c = comb(m, t)
            shift = (t * r) % d
            for j in range(0, 4 - t):
                for s, v in dp[j].items():
                    ndp[j + t][(s + shift) % d] += v * c
        dp = ndp
    return dp[3][0]
