# Binary search the limit between max(pages) and sum(pages), greedily counting days for feasibility.
from typing import List, Optional, Any


def _days_needed(pages: List[int], limit: int) -> int:
    used = 1
    current = 0
    for p in pages:
        if current + p <= limit:
            current += p
        else:
            used += 1
            current = p
    return used


def minimumDailyPrintingLimit(pages: List[int], days: int) -> int:
    if not pages:
        return 0
    lo, hi = max(pages), sum(pages)
    while lo < hi:
        mid = (lo + hi) // 2
        if _days_needed(pages, mid) <= days:
            hi = mid
        else:
            lo = mid + 1
    return lo
