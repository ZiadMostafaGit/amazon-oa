# Prefix sum of the transaction array up to and including selectedDay.
from typing import List, Optional, Any


def balanceOnDay(transactions: List[int], selectedDay: int) -> int:
    if selectedDay < 0:
        return 0
    end = min(selectedDay, len(transactions) - 1)
    total = 0
    for i in range(end + 1):
        total += transactions[i]
    return total
