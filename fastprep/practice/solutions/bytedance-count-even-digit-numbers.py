# Count values whose decimal representation has an even length.
from typing import List, Optional, Any


def countEvenDigitNumbers(numbers: List[int]) -> int:
    return sum(1 for value in numbers if len(str(abs(value))) % 2 == 0)
