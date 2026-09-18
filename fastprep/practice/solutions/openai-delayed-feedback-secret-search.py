# Replay the binary search: submit the lower midpoint first, then apply the pending response to the previous guess.
from typing import List, Optional, Any


def findSecretFromDelayedFeedback(upperBound: int, feedback: List[int]) -> int:
    low, high = 1, upperBound
    prev = None
    for resp in feedback:
        guess = low + (high - low) // 2
        if resp == 2:
            prev = guess
            continue
        if resp == 0:
            return prev
        if resp == 1:
            if prev + 1 > low:
                low = prev + 1
        else:
            if prev - 1 < high:
                high = prev - 1
        prev = guess
    return prev
