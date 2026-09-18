# Subset-XOR reachability DP over the value range [0,100], then greedy lex-smallest reconstruction.
from typing import List, Optional, Any

_MAXV = 100
_BITS = 128  # every value <= 100 < 128, so all XORs stay below 128


def _reachable(kmax: int):
    # f[i][c][x] -> can we pick c distinct values from i..100 whose XOR is x?
    f = [[bytearray(_BITS) for _ in range(kmax + 1)] for _ in range(_MAXV + 2)]
    f[_MAXV + 1][0][0] = 1
    for i in range(_MAXV, -1, -1):
        for c in range(kmax + 1):
            row = f[i][c]
            prev = f[i + 1][c]
            row[:] = prev
            if c:
                take = f[i + 1][c - 1]
                for x in range(_BITS):
                    if take[x]:
                        row[x ^ i] = 1
    return f


def assignLetterValues(s: str) -> List[int]:
    freq = {}
    for ch in s:
        freq[ch] = freq.get(ch, 0) + 1
    odd = sorted(ch for ch in freq if freq[ch] % 2 == 1)
    even = sorted(ch for ch in freq if freq[ch] % 2 == 0)
    k = len(odd)

    chosen: List[int] = []
    if k:
        f = _reachable(k)
        best = next(x for x in range(_BITS) if f[0][k][x])
        cur = 0
        remaining = k
        v = 0
        while remaining:
            while v <= _MAXV:
                if f[v + 1][remaining - 1][best ^ cur ^ v]:
                    break
                v += 1
            chosen.append(v)
            cur ^= v
            remaining -= 1
            v += 1

    used = set(chosen)
    result = list(chosen)
    nxt = 0
    for _ in even:
        while nxt in used:
            nxt += 1
        used.add(nxt)
        result.append(nxt)
    return result
