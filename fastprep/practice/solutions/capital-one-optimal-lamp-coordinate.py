# Sliding window over the sorted coordinates; the first widest window gives the smallest lamp spot.
from typing import List, Optional, Any


def optimalLampCoordinate(objects: List[int], radius: int) -> int:
    span = 2 * radius
    best_count = 0
    best_coord = objects[0] - radius
    i = 0
    for j in range(len(objects)):
        while objects[j] - objects[i] > span:
            i += 1
        count = j - i + 1
        if count > best_count:
            best_count = count
            best_coord = objects[j] - radius
    return best_coord
