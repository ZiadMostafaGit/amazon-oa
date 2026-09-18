# Weighted interval scheduling: sort by end time, binary search the last show finishing strictly before the start, DP.
from typing import List, Optional, Any
from bisect import bisect_left


def cinemaShows(start: List[int], duration: List[int], volume: List[int]) -> int:
    shows = sorted(
        ((start[i] + duration[i], start[i], volume[i]) for i in range(len(start)))
    )
    ends = [s[0] for s in shows]
    # dp[i] = best volume using the first i shows (by end order)
    dp = [0] * (len(shows) + 1)
    for i, (_end, s, vol) in enumerate(shows):
        j = bisect_left(ends, s, 0, i)  # shows with end < s (strict gap required)
        best_with = dp[j] + vol
        dp[i + 1] = dp[i] if dp[i] > best_with else best_with
    return dp[len(shows)]
