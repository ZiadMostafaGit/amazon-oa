# XOR swap in place: no third scalar holds either value.
from typing import List, Optional, Any


def swapWithoutTemporary(a: int, b: int) -> List[int]:
    a ^= b
    b ^= a
    a ^= b
    return [a, b]
