# Per-type FIFO queues of arrival days; greedily pick the pair whose second arrival is earliest, then the oldest leftover.
from typing import List, Optional, Any
from collections import deque


def canCookByDay(ingredients: List[str]) -> List[int]:
    stock = {}
    total = 0
    res = []
    for day, kind in enumerate(ingredients):
        stock.setdefault(kind, deque()).append(day)
        total += 1
        if total < 3:
            res.append(0)
            continue
        # pick the type whose second-oldest in-stock item arrived earliest
        best_type = None
        best_day = None
        for t, q in stock.items():
            if len(q) >= 2:
                if best_day is None or q[1] < best_day:
                    best_day = q[1]
                    best_type = t
        if best_type is None:
            res.append(0)
            continue
        q = stock[best_type]
        q.popleft()
        q.popleft()
        # third ingredient: oldest remaining of any type
        third_type = None
        third_day = None
        for t, qq in stock.items():
            if qq and (third_day is None or qq[0] < third_day):
                third_day = qq[0]
                third_type = t
        stock[third_type].popleft()
        total -= 3
        res.append(1)
    return res
