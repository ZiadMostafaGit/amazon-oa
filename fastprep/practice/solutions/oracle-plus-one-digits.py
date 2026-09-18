# Right-to-left carry propagation on the fixed-size digit array, prepending 1 only on full overflow.
from typing import List, Optional, Any


def plusOne(digits: List[int]) -> List[int]:
    i = len(digits) - 1
    while i >= 0:
        if digits[i] < 9:
            digits[i] += 1
            return digits
        digits[i] = 0
        i -= 1
    # every digit was 9: the result is 1 followed by all zeros
    return [1] + digits
