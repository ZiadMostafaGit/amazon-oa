# Single pass: count adjacent pairs whose case-folded letters differ.
from typing import List, Optional, Any


def countKeyChanges(recording: List[str]) -> int:
    changes = 0
    for i in range(1, len(recording)):
        if recording[i].lower() != recording[i - 1].lower():
            changes += 1
    return changes
