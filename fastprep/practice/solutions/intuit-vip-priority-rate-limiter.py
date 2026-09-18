# Bucket requests by fixed period, then admit VIPs before normals in stable arrival order.
from typing import List, Optional, Any


def admitVipPriorityRequests(requests: List[List[int]], periodLength: int) -> List[bool]:
    CAPACITY = 5
    result = [False] * len(requests)
    periods = {}
    order = []
    for i, req in enumerate(requests):
        q = req[0] // periodLength
        bucket = periods.get(q)
        if bucket is None:
            bucket = ([], [])
            periods[q] = bucket
            order.append(q)
        bucket[0 if req[2] == 1 else 1].append(i)

    for q in order:
        vips, normals = periods[q]
        slots = CAPACITY
        for i in vips:
            if slots == 0:
                break
            result[i] = True
            slots -= 1
        for i in normals:
            if slots == 0:
                break
            result[i] = True
            slots -= 1
    return result
