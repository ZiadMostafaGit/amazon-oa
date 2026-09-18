# Simulate the operation stream, keeping per-customer totals and sorting on each query.
from typing import List, Optional, Any


def processCustomerRevenueOperations(operations: List[List[str]]) -> List[List[int]]:
    totals: List[int] = []
    out: List[List[int]] = []
    for op in operations:
        name = op[0]
        if name == "ADD":
            revenue = int(op[1])
            cid = len(totals)
            totals.append(revenue)
            out.append([cid])
        elif name == "ADD_WITH_REFERRER":
            revenue = int(op[1])
            referrer = int(op[2])
            cid = len(totals)
            totals.append(revenue)
            totals[referrer] += revenue
            out.append([cid])
        else:
            k = int(op[1])
            threshold = int(op[2])
            eligible = [(t, i) for i, t in enumerate(totals) if t >= threshold]
            eligible.sort()
            out.append([i for _, i in eligible[:k]])
    return out
