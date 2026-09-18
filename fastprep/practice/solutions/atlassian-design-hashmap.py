# Separate-chaining hash map over a fixed bucket array, replayed over the operation list.
from typing import List, Optional, Any


class _HashMap:
    def __init__(self, size: int = 4099) -> None:
        self.size = size
        self.buckets: List[List[List[int]]] = [[] for _ in range(size)]

    def _index(self, key: int) -> int:
        return key % self.size

    def put(self, key: int, value: int) -> None:
        bucket = self.buckets[self._index(key)]
        for pair in bucket:
            if pair[0] == key:
                pair[1] = value
                return
        bucket.append([key, value])

    def get(self, key: int) -> int:
        bucket = self.buckets[self._index(key)]
        for pair in bucket:
            if pair[0] == key:
                return pair[1]
        return -1

    def remove(self, key: int) -> None:
        bucket = self.buckets[self._index(key)]
        for i, pair in enumerate(bucket):
            if pair[0] == key:
                bucket.pop(i)
                return


def runHashMap(operations: List[str], keys: List[int], values: List[int]) -> List[str]:
    hashmap = _HashMap()
    output: List[str] = []
    for i, op in enumerate(operations):
        if op == "put":
            hashmap.put(keys[i], values[i])
            output.append("null")
        elif op == "get":
            output.append(str(hashmap.get(keys[i])))
        elif op == "remove":
            hashmap.remove(keys[i])
            output.append("null")
        else:
            output.append("null")
    return output
