# Maintain a set of occupied locations, applying each move, then sort.
from typing import List, Optional, Any


def getFinalLocations(locations: List[int], movedFrom: List[int], movedTo: List[int]) -> List[int]:
    occupied = set(locations)
    for src, dst in zip(movedFrom, movedTo):
        occupied.discard(src)
        occupied.add(dst)
    return sorted(occupied)
