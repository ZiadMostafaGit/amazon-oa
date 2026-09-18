# Approach: sort levels, then greedily open a new class whenever the current level exceeds the class anchor by more than maxSpread.
from typing import List, Optional, Any


def groupStudents(levels: List[int], maxSpread: int) -> int:
    if not levels:
        return 0
    order = sorted(levels)
    classes = 1
    anchor = order[0]
    for lv in order:
        if lv - anchor > maxSpread:
            classes += 1
            anchor = lv
    return classes
