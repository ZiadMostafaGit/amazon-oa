# Prefix sums of populations plus binary search for the ticket's owning range.
import bisect
from typing import List, Optional, Any


def selectCityByPopulation(cities: List[str], populations: List[int], ticket: int) -> str:
    prefix = []
    running = 0
    for p in populations:
        running += p
        prefix.append(running)
    idx = bisect.bisect_right(prefix, ticket)
    if idx >= len(cities):
        idx = len(cities) - 1
    return cities[idx]
