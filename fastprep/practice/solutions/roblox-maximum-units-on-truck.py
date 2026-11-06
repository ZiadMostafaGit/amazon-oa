# Sort box types by units per box, descending, and fill the truck from the richest type.
from typing import List, Optional, Any


def maximumTruckUnits(boxes: List[int], unitsPerBox: List[int], capacity: int) -> int:
    total = 0
    for units, count in sorted(zip(unitsPerBox, boxes), reverse=True):
        if capacity <= 0:
            break
        take = min(count, capacity)
        total += take * units
        capacity -= take
    return total
