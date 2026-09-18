# Hash set of (field index, value) pairs over underwriting rows only.
from typing import List, Optional, Any


def countDistinctUnderwritingPii(events: List[List[str]]) -> int:
    seen = set()
    for row in events:
        if not row or row[0] != "underwriting":
            continue
        for idx in range(1, min(5, len(row))):
            value = row[idx]
            if value:
                seen.add((idx, value))
    return len(seen)
