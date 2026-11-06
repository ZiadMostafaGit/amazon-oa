# bits(i) = bits(i >> 1) + (i & 1): dropping the last bit gives a smaller, already-computed number.
from typing import List


def countBits(n: int) -> List[int]:
    res = [0] * (n + 1)
    for i in range(1, n + 1):
        res[i] = res[i >> 1] + (i & 1)
    return res
