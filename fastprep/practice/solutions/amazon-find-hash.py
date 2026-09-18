# Greedy: sort the moduli ascending and assign the smallest unused residue that each modulus still allows.
from typing import List, Optional, Any


def findHash(param: List[int]) -> int:
    cur = 0
    for p in sorted(param):
        if cur < p:
            cur += 1
    return cur
