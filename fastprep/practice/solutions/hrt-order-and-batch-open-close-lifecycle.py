# Hash maps from order id to open/close time and from batch id to its orders, then aggregate.
from typing import List, Optional, Any


def getLifecycleWindow(openTimestamps: List[int], openOrderIds: List[str], openBatchIds: List[str], closeTimestamps: List[int], closeOrderIds: List[str], closeBatchIds: List[str], queryType: str, queryId: str) -> List[int]:
    open_at = {}
    batch_orders = {}
    for i, oid in enumerate(openOrderIds):
        open_at[oid] = openTimestamps[i]
        batch_orders.setdefault(openBatchIds[i], []).append(oid)
    close_at = {}
    for i, oid in enumerate(closeOrderIds):
        close_at[oid] = closeTimestamps[i]

    if queryType == "ORDER":
        return [open_at[queryId], close_at.get(queryId, 0)]

    orders = batch_orders.get(queryId, [])
    if not orders:
        return [0, 0]
    start = min(open_at[o] for o in orders)
    if any(o not in close_at for o in orders):
        return [start, 0]
    return [start, max(close_at[o] for o in orders)]
