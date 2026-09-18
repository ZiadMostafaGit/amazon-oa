# Approach: linear scan for the first line containing "ERROR", then slice a
# clamped window of two lines on each side.
from typing import List, Optional, Any


def extractErrorContext(lines: List[str]) -> List[str]:
    for i, line in enumerate(lines):
        if "ERROR" in line:
            start = max(0, i - 2)
            end = min(len(lines), i + 3)
            return list(lines[start:end])
    return []
