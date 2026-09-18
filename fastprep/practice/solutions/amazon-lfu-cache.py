# Approach: LFU cache with freq -> OrderedDict buckets and a running min-frequency pointer (O(1) per op).
from collections import OrderedDict, defaultdict
from typing import List, Optional, Any


class LFUCache:
    def __init__(self, capacity: int) -> None:
        self.cap = capacity
        self.vals = {}
        self.freq = {}
        self.buckets = defaultdict(OrderedDict)
        self.minf = 0

    def _touch(self, key: int) -> None:
        f = self.freq[key]
        del self.buckets[f][key]
        if not self.buckets[f]:
            del self.buckets[f]
            if self.minf == f:
                self.minf = f + 1
        self.freq[key] = f + 1
        self.buckets[f + 1][key] = None

    def get(self, key: int) -> int:
        if key not in self.vals:
            return -1
        self._touch(key)
        return self.vals[key]

    def put(self, key: int, value: int) -> None:
        if self.cap <= 0:
            return
        if key in self.vals:
            self.vals[key] = value
            self._touch(key)
            return
        if len(self.vals) >= self.cap:
            evict, _ = self.buckets[self.minf].popitem(last=False)
            if not self.buckets[self.minf]:
                del self.buckets[self.minf]
            del self.vals[evict]
            del self.freq[evict]
        self.vals[key] = value
        self.freq[key] = 1
        self.buckets[1][key] = None
        self.minf = 1


def solve(capacity: int, operations: List[str]) -> List[int]:
    cache = LFUCache(capacity)
    out: List[int] = []
    for op in operations:
        parts = op.split()
        if parts[0] == "put":
            cache.put(int(parts[1]), int(parts[2]))
        else:
            out.append(cache.get(int(parts[1])))
    return out
