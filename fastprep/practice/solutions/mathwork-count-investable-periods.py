# Sliding-window counting: for each right end, valid lefts lie after the last out-of-range
# element and at or before the most recent occurrences of both min_price and max_price.
from typing import List, Optional, Any


def countInvestablePeriods(price: List[int], max_price: int, min_price: int) -> int:
    last_bad = -1   # last index holding a value outside [min_price, max_price]
    last_min = -1   # last index holding exactly min_price
    last_max = -1   # last index holding exactly max_price
    total = 0
    for i, v in enumerate(price):
        if v < min_price or v > max_price:
            last_bad = i
        if v == min_price:
            last_min = i
        if v == max_price:
            last_max = i
        limit = last_min if last_min < last_max else last_max
        if limit > last_bad:
            total += limit - last_bad
    return total
