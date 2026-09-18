# LFU cache with frequency buckets of OrderedDicts plus a running minimum frequency (O(1) amortized).
from collections import OrderedDict
from typing import List, Optional, Any


class _LFU:
    def __init__(self, capacity: int):
        self.capacity = capacity
        self.vals = {}
        self.freqs = {}
        self.buckets = {}
        self.min_freq = 0

    def _touch(self, key: int) -> None:
        f = self.freqs[key]
        bucket = self.buckets[f]
        del bucket[key]
        if not bucket:
            del self.buckets[f]
            if self.min_freq == f:
                self.min_freq = f + 1
        self.freqs[key] = f + 1
        self.buckets.setdefault(f + 1, OrderedDict())[key] = None

    def get(self, key: int) -> int:
        if key not in self.vals:
            return -1
        self._touch(key)
        return self.vals[key]

    def put(self, key: int, value: int) -> None:
        if self.capacity <= 0:
            return
        if key in self.vals:
            self.vals[key] = value
            self._touch(key)
            return
        if len(self.vals) >= self.capacity:
            bucket = self.buckets[self.min_freq]
            evicted, _ = bucket.popitem(last=False)
            if not bucket:
                del self.buckets[self.min_freq]
            del self.vals[evicted]
            del self.freqs[evicted]
        self.vals[key] = value
        self.freqs[key] = 1
        self.buckets.setdefault(1, OrderedDict())[key] = None
        self.min_freq = 1


def processLfuCache(capacity: int, operations: List[str]) -> List[int]:
    cache = _LFU(capacity)
    out = []
    for op in operations:
        parts = op.split()
        if parts[0] == "get":
            out.append(cache.get(int(parts[1])))
        else:
            cache.put(int(parts[1]), int(parts[2]))
    return out
