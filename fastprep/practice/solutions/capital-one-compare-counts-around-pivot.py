# Single linear pass counting values strictly above and below the pivot.
from typing import List, Optional, Any


def solution(numbers: List[int], pivot: int) -> str:
    greater = 0
    less = 0
    for n in numbers:
        if n > pivot:
            greater += 1
        elif n < pivot:
            less += 1
    if greater > less:
        return "greater"
    if greater < less:
        return "smaller"
    return "tie"
