# Greedy exchange argument: order by (worstCase - expected) descending, then take the max prefix requirement.
from typing import List, Optional, Any


def plenProduction(worstCase: List[int], expected: List[int]) -> int:
    n = len(worstCase)
    if n == 0:
        return 0
    order = sorted(range(n), key=lambda i: worstCase[i] - expected[i], reverse=True)
    need = 0
    spent = 0
    for i in order:
        req = spent + worstCase[i]
        if req > need:
            need = req
        spent += expected[i]
    if spent > need:
        need = spent
    return need
