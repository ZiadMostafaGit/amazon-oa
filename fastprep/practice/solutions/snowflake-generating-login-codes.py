# Two-pointer greedy over prefix sums: count common prefix-sum boundaries.
from typing import List, Optional, Any


def getLoginCodes(initialLogin: List[int], standardLogin: List[int]) -> int:
    n, m = len(initialLogin), len(standardLogin)
    if sum(initialLogin) != sum(standardLogin):
        return -1
    i = j = 0
    a = b = 0
    count = 0
    while i < n and j < m:
        a += initialLogin[i]
        i += 1
        b += standardLogin[j]
        j += 1
        while a != b:
            if a < b:
                if i >= n:
                    break
                a += initialLogin[i]
                i += 1
            else:
                if j >= m:
                    break
                b += standardLogin[j]
                j += 1
        if a == b:
            count += 1
    return count if count > 0 else -1
