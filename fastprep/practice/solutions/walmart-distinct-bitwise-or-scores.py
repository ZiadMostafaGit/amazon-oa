# DP over values with reachable-OR sets held as 1024-bit integers, prefix-OR Fenwick tree for "all smaller values".
from typing import List, Optional, Any

_LIMIT = 1024
_BITS = 10
_ONE = []
_ZERO = []
for _b in range(_BITS):
    _one = 0
    _zero = 0
    for _i in range(_LIMIT):
        if (_i >> _b) & 1:
            _one |= 1 << _i
        else:
            _zero |= 1 << _i
    _ONE.append(_one)
    _ZERO.append(_zero)


def getDistinctScorsValues(arr: List[int]) -> List[int]:
    # Fenwick tree over values 0.._LIMIT-1 supporting prefix OR of reachable-set masks.
    tree = [0] * (_LIMIT + 1)

    def update(pos: int, mask: int) -> None:
        i = pos + 1
        while i <= _LIMIT:
            tree[i] |= mask
            i += i & (-i)

    def prefix(pos: int) -> int:
        # OR of masks for values 0..pos-1
        res = 0
        i = pos
        while i > 0:
            res |= tree[i]
            i -= i & (-i)
        return res

    total = 1  # the empty subsequence scores 0
    for x in arr:
        reach = prefix(x)  # ORs of increasing subsequences ending in a value < x
        if reach:
            for b in range(_BITS):
                if (x >> b) & 1:
                    reach = (reach & _ONE[b]) | ((reach & _ZERO[b]) << (1 << b))
        cur = reach | (1 << x)
        total |= cur
        update(x, cur)

    out = []
    v = 0
    while total:
        low = total & (-total)
        out.append(low.bit_length() - 1)
        total ^= low
    return out
