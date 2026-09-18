# Flatten pages and count values inside the inclusive bounds.
from typing import List, Optional, Any


def countMedicalRecordsInRange(pages: List[List[int]], lowerBound: int, upperBound: int) -> int:
    total = 0
    for page in pages:
        for value in page:
            if lowerBound <= value <= upperBound:
                total += 1
    return total
