# Sort; a valid selection is a run where neighbouring sorted values differ by at most 1. Longest such run. O(n log n).
from typing import List, Optional, Any


def maxTickets(tickets: List[int]) -> int:
    t = sorted(tickets)
    best = run = 1
    for i in range(1, len(t)):
        run = run + 1 if t[i] - t[i - 1] <= 1 else 1
        best = max(best, run)
    return best
