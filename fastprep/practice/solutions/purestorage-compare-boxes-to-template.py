# Count pairs whose multiset of characters differs, using Counter on each side.
from typing import List, Optional, Any
from collections import Counter


def countMismatchedBoxes(boxes: List[List[str]]) -> int:
    mismatches = 0
    for pair in boxes:
        box, template = pair[0], pair[1]
        if Counter(box) != Counter(template):
            mismatches += 1
    return mismatches
