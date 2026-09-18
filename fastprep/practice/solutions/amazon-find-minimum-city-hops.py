# BFS over wildcard-pattern buckets so neighbours are found without pairwise comparison.
from collections import defaultdict, deque
from typing import List, Optional, Any


def findMinimumCityHops(cities: List[str], startCity: str, endCity: str) -> int:
    unique = set(cities)
    if startCity not in unique or endCity not in unique:
        return -1
    if startCity == endCity:
        return 0
    buckets = defaultdict(list)
    for city in unique:
        for i in range(len(city)):
            buckets[city[:i] + "*" + city[i + 1:]].append(city)
    visited = {startCity}
    queue = deque([(startCity, 0)])
    while queue:
        city, dist = queue.popleft()
        for i in range(len(city)):
            pattern = city[:i] + "*" + city[i + 1:]
            for nxt in buckets[pattern]:
                if nxt in visited:
                    continue
                if nxt == endCity:
                    return dist + 1
                visited.add(nxt)
                queue.append((nxt, dist + 1))
    return -1
