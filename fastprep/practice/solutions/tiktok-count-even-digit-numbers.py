# Count values whose decimal representation has an even length.
from typing import List


def solution(numbers: List[int]) -> int:
    return sum(1 for x in numbers if len(str(x)) % 2 == 0)
