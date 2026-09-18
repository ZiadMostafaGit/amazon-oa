# O(1) LFU cache: frequency buckets of OrderedDicts with a running minimum frequency.
from collections import OrderedDict, defaultdict
from typing import List, Optional, Any


def processLfuCache(capacity: int, operations: List[str]) -> List[int]:
    vals = {}                       # key -> value
    freq = {}                       # key -> frequency
    buckets = defaultdict(OrderedDict)  # freq -> ordered keys, oldest first
    min_freq = 0
    out = []

    def touch(key: int) -> None:
        nonlocal min_freq
        f = freq[key]
        del buckets[f][key]
        if not buckets[f]:
            del buckets[f]
            if min_freq == f:
                min_freq = f + 1
        freq[key] = f + 1
        buckets[f + 1][key] = None

    for op in operations:
        parts = op.split()
        if parts[0] == 'get':
            key = int(parts[1])
            if key in vals:
                touch(key)
                out.append(vals[key])
            else:
                out.append(-1)
        else:
            key, value = int(parts[1]), int(parts[2])
            if capacity <= 0:
                continue
            if key in vals:
                vals[key] = value
                touch(key)
                continue
            if len(vals) >= capacity:
                evict, _ = buckets[min_freq].popitem(last=False)
                if not buckets[min_freq]:
                    del buckets[min_freq]
                del vals[evict]
                del freq[evict]
            vals[key] = value
            freq[key] = 1
            buckets[1][key] = None
            min_freq = 1
    return out
