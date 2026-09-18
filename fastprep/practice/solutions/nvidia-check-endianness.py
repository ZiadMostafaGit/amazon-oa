# Rebuild the integer from both byte orders and compare against the target, preferring little-endian on a tie.
from typing import List, Optional, Any


def checkEndianness(bytes: List[int], value: int) -> str:
    n = len(bytes)
    little = 0
    big = 0
    for i, b in enumerate(bytes):
        little |= b << (8 * i)
        big |= b << (8 * (n - 1 - i))
    if little == value:
        return "little"
    if big == value:
        return "big"
    return "neither"
