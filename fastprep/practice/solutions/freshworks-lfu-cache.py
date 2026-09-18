# LFU cache with per-frequency ordered buckets and a running minimum frequency.
from typing import List, Optional, Any
from collections import OrderedDict, defaultdict


def processLfuCommands(capacity: int, operations: List[str]) -> List[int]:
    vals = {}          # key -> value
    freq = {}          # key -> frequency
    buckets = defaultdict(OrderedDict)   # frequency -> ordered keys (LRU first)
    min_freq = 0
    results: List[int] = []

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
                results.append(vals[key])
            else:
                results.append(-1)
        else:
            key = int(parts[1])
            value = int(parts[2])
            if key in vals:
                vals[key] = value
                touch(key)
                continue
            if len(vals) >= capacity:
                victim, _ = buckets[min_freq].popitem(last=False)
                if not buckets[min_freq]:
                    del buckets[min_freq]
                del vals[victim]
                del freq[victim]
            vals[key] = value
            freq[key] = 1
            buckets[1][key] = None
            min_freq = 1
    return results
