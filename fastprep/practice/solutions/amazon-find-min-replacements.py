# Counting: pick the best (most frequent) value for even and odd index groups, with the two values forced distinct.
from typing import List, Optional, Any
from collections import Counter


def _top2(counter: Counter):
    # returns [(value, count), (value, count)] padded with (None, 0)
    items = counter.most_common(2)
    while len(items) < 2:
        items.append((None, 0))
    return items


def findMinReplacements(parcels: List[int]) -> int:
    n = len(parcels)
    even = Counter(parcels[0::2])
    odd = Counter(parcels[1::2])
    ne = len(parcels[0::2])
    no = n - ne

    (e1v, e1c), (e2v, e2c) = _top2(even)
    (o1v, o1c), (o2v, o2c) = _top2(odd)

    if e1v != o1v:
        keep = e1c + o1c
    else:
        keep = max(e1c + o2c, e2c + o1c)

    return n - keep
