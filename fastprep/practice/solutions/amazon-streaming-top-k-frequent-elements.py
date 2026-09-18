# Frequency-bucket approach: counts + per-frequency sorted value lists, walked top-down each step.
from typing import List, Optional, Any
from bisect import bisect_left, insort


def topKAfterEach(stream: List[int], k: int) -> List[List[int]]:
    count = {}
    bucket = {}          # frequency -> sorted list of values having that frequency
    freqs = []           # ascending sorted list of frequencies with a non-empty bucket
    out = []

    for v in stream:
        old = count.get(v, 0)
        new = old + 1
        count[v] = new

        if old > 0:
            b = bucket[old]
            b.pop(bisect_left(b, v))
            if not b:
                del bucket[old]
                freqs.pop(bisect_left(freqs, old))

        b = bucket.get(new)
        if b is None:
            b = []
            bucket[new] = b
            insort(freqs, new)
        insort(b, v)

        row = []
        for i in range(len(freqs) - 1, -1, -1):
            vals = bucket[freqs[i]]
            need = k - len(row)
            if need <= 0:
                break
            row.extend(vals[:need])
            if len(row) >= k:
                break
        out.append(row)

    return out
