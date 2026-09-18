# House Robber: linear DP tracking best totals including vs excluding current house.
from typing import List, Optional, Any


def solve(values: List[int]) -> int:
    incl = 0  # best total that may use the previous house
    excl = 0  # best total that does not use the previous house
    for v in values:
        take = excl + v
        skip = incl if incl > excl else excl
        incl, excl = take, skip
    return incl if incl > excl else excl
