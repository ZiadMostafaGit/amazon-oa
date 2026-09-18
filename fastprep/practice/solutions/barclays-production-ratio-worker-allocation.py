# Direct arithmetic: split total by the ratio parts, then divide each quantity by its per-worker rate.
from typing import List, Optional, Any


def allocateWorkers(total: int, firstRatio: int, secondRatio: int, firstRate: int, secondRate: int) -> List[int]:
    parts = firstRatio + secondRatio
    firstQty = total * firstRatio // parts
    secondQty = total * secondRatio // parts
    return [firstQty // firstRate, secondQty // secondRate]
