# Concatenate both arrays and sort (inputs are not guaranteed sorted).
from typing import List, Optional, Any


def mergeTwoArraysSorted(a: List[int], b: List[int]) -> List[int]:
    return sorted(a + b)
