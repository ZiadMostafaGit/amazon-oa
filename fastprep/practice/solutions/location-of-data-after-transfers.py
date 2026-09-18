# Maintain a set of occupied locations, applying each move in order.
from typing import List, Optional, Any


def locationOfDataAfterTransfers(locations: List[int], movedFrom: List[int], movedTo: List[int]) -> List[int]:
    occupied = set(locations)
    for src, dst in zip(movedFrom, movedTo):
        occupied.discard(src)
        occupied.add(dst)
    return sorted(occupied)
