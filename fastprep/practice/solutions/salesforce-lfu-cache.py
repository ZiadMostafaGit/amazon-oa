# LFU cache: hash map of key->(value,freq) plus per-frequency OrderedDict buckets and a min-freq pointer.
from typing import List, Optional, Any
from collections import OrderedDict, defaultdict


def processLfuCache(capacity: int, operations: List[str]) -> List[int]:
    vals = {}                            # key -> value
    freqs = {}                           # key -> frequency
    buckets = defaultdict(OrderedDict)   # freq -> OrderedDict of keys, oldest first
    min_freq = 0
    out: List[int] = []

    def touch(key: int) -> None:
        nonlocal min_freq
        f = freqs[key]
        del buckets[f][key]
        if not buckets[f]:
            del buckets[f]
            if min_freq == f:
                min_freq = f + 1
        freqs[key] = f + 1
        buckets[f + 1][key] = None

    for op in operations:
        parts = op.split()
        cmd = parts[0].lower()
        if cmd == "get":
            key = int(parts[1])
            if key in vals:
                touch(key)
                out.append(vals[key])
            else:
                out.append(-1)
        else:
            key = int(parts[1])
            value = int(parts[2])
            if key in vals:
                vals[key] = value
                touch(key)
                continue
            if capacity <= 0:
                continue
            if len(vals) >= capacity:
                evict, _ = buckets[min_freq].popitem(last=False)
                if not buckets[min_freq]:
                    del buckets[min_freq]
                del vals[evict]
                del freqs[evict]
            vals[key] = value
            freqs[key] = 1
            buckets[1][key] = None
            min_freq = 1
    return out
