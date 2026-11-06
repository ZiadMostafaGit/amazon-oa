from typing import List, Optional, Any


def solution(recording: List[str]) -> int:
    changes = 0
    for i in range(1, len(recording)):
        if recording[i].lower() != recording[i - 1].lower():
            changes += 1
    return changes
