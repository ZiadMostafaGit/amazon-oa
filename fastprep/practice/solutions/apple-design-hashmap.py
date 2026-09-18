# Hand-built hash table: fixed bucket array with separate chaining (lists of [key, value]).
from typing import List, Optional, Any


class _MyHashMap:
    def __init__(self, capacity: int = 4093) -> None:
        self._cap = capacity
        self._buckets: List[List[List[int]]] = [[] for _ in range(capacity)]

    def _index(self, key: int) -> int:
        return (key * 2654435761) % self._cap

    def put(self, key: int, value: int) -> None:
        bucket = self._buckets[self._index(key)]
        for entry in bucket:
            if entry[0] == key:
                entry[1] = value
                return
        bucket.append([key, value])

    def get(self, key: int) -> int:
        bucket = self._buckets[self._index(key)]
        for entry in bucket:
            if entry[0] == key:
                return entry[1]
        return -1

    def remove(self, key: int) -> None:
        bucket = self._buckets[self._index(key)]
        for i in range(len(bucket)):
            if bucket[i][0] == key:
                bucket[i] = bucket[-1]
                bucket.pop()
                return


def runHashMap(operations: List[str], keys: List[int], values: List[int]) -> List[int]:
    table = _MyHashMap()
    result: List[int] = []
    for i, op in enumerate(operations):
        if op == "put":
            table.put(keys[i], values[i])
        elif op == "get":
            result.append(table.get(keys[i]))
        elif op == "remove":
            table.remove(keys[i])
    return result
