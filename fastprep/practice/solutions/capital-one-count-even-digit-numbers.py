# Parse whitespace-separated integers and count those whose decimal length is even.
from typing import List, Optional, Any


def solveOneCountEvenDigitNumbers(input: str) -> List[str]:
    tokens = input.split()
    count = 0
    for t in tokens:
        n = int(t)
        if len(str(abs(n))) % 2 == 0:
            count += 1
    return [str(count)]
