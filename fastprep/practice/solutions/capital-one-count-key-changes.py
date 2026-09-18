# Single pass comparing each character with the previous one, case-insensitively.
from typing import List, Optional, Any


def countKeyChanges(recording: List[str]) -> int:
    changes = 0
    prev = None
    for ch in recording:
        key = str(ch).lower()
        if prev is not None and key != prev:
            changes += 1
        prev = key
    return changes
