from typing import List, Optional, Any
from bisect import bisect_left


def longestChosenSubsequence(first: List[int], second: List[int]) -> int:
    # tails[k] = smallest possible last value of a strictly increasing
    # subsequence of length k + 1 using the positions seen so far.
    tails: List[int] = []
    for a, b in zip(first, second):
        # Both options are placed against the tails from before this index,
        # so one index never contributes two values to the same subsequence.
        updates = []
        for v in {a, b}:
            updates.append((bisect_left(tails, v), v))
        for p, v in updates:
            if p == len(tails):
                tails.append(v)
            elif v < tails[p]:
                tails[p] = v
    return len(tails)
