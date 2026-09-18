# Min-heap keyed on (active connections, target index) to pick the least-loaded target each time.
import heapq
from typing import List, Optional, Any


def routeRequests(numTargets: int, maxConnectionsPerTarget: int, requests: List[str]) -> List[str]:
    heap = [(0, i) for i in range(1, numTargets + 1)]
    heapq.heapify(heap)
    out: List[str] = []
    for req in requests:
        parts = req.split(",")
        if not parts or parts[0] != "CONNECT":
            continue
        connection_id = parts[1]
        user_id = parts[2]
        load, idx = heapq.heappop(heap)
        heapq.heappush(heap, (load + 1, idx))
        out.append(connection_id + "," + user_id + "," + str(idx))
    return out
