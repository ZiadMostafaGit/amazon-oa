# Maintain sorted disjoint intervals; binary-search the touching range and merge it in place.
from bisect import bisect_left, bisect_right
from typing import List, Optional, Any


def trackReceivedByteRanges(chunks: List[List[int]]) -> List[List[str]]:
    starts: List[int] = []
    ends: List[int] = []
    snapshots: List[List[str]] = []

    for chunk in chunks:
        l, r = int(chunk[0]), int(chunk[1])
        # first interval whose end can touch the new chunk (adjacent counts)
        i = bisect_left(ends, l - 1)
        # last interval whose start can touch the new chunk
        j = bisect_right(starts, r + 1) - 1
        if i <= j:
            new_l = min(l, starts[i])
            new_r = max(r, ends[j])
            starts[i:j + 1] = [new_l]
            ends[i:j + 1] = [new_r]
        else:
            starts.insert(i, l)
            ends.insert(i, r)
        snapshots.append(["%d:%d" % (s, e) for s, e in zip(starts, ends)])

    return snapshots
