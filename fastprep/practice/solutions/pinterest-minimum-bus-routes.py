# Approach: BFS over bus routes, using a stop -> routes index to expand one bus at a time.
from typing import List, Optional, Any
from collections import defaultdict, deque


def minimumBusRoutes(routes: List[List[int]], sourceStop: int, targetStop: int) -> int:
    if sourceStop == targetStop:
        return 0
    stop_to_routes = defaultdict(list)
    for i, route in enumerate(routes):
        for stop in route:
            stop_to_routes[stop].append(i)
    if sourceStop not in stop_to_routes or targetStop not in stop_to_routes:
        return -1
    visited_routes = set()
    visited_stops = {sourceStop}
    queue = deque([(sourceStop, 0)])
    while queue:
        stop, buses = queue.popleft()
        for r in stop_to_routes[stop]:
            if r in visited_routes:
                continue
            visited_routes.add(r)
            for nxt in routes[r]:
                if nxt == targetStop:
                    return buses + 1
                if nxt not in visited_stops:
                    visited_stops.add(nxt)
                    queue.append((nxt, buses + 1))
    return -1
