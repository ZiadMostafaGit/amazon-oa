# Hand-built separate-chaining hash table with bucket lists and key comparison on collision.
from typing import List, Optional, Any


class _HashMap:
    def __init__(self, capacity: int = 1024) -> None:
        self._capacity = capacity
        self._size = 0
        self._buckets: List[Optional[List[List[int]]]] = [None] * capacity

    def _index(self, key: int) -> int:
        h = (key * 2654435761) ^ (key >> 16)
        return h % self._capacity

    def _grow(self) -> None:
        old = self._buckets
        self._capacity *= 2
        self._buckets = [None] * self._capacity
        for bucket in old:
            if bucket:
                for pair in bucket:
                    idx = self._index(pair[0])
                    if self._buckets[idx] is None:
                        self._buckets[idx] = []
                    self._buckets[idx].append(pair)

    def put(self, key: int, value: int) -> None:
        idx = self._index(key)
        bucket = self._buckets[idx]
        if bucket is None:
            bucket = []
            self._buckets[idx] = bucket
        for pair in bucket:
            if pair[0] == key:
                pair[1] = value
                return
        bucket.append([key, value])
        self._size += 1
        if self._size > self._capacity:
            self._grow()

    def get(self, key: int) -> int:
        bucket = self._buckets[self._index(key)]
        if bucket:
            for pair in bucket:
                if pair[0] == key:
                    return pair[1]
        return -1

    def remove(self, key: int) -> None:
        idx = self._index(key)
        bucket = self._buckets[idx]
        if not bucket:
            return
        for i, pair in enumerate(bucket):
            if pair[0] == key:
                bucket[i] = bucket[-1]
                bucket.pop()
                self._size -= 1
                return


def runHashMap(operations: List[str], arguments: List[List[int]]) -> List[int]:
    table = _HashMap()
    answer = []
    for op, args in zip(operations, arguments):
        if op == "put":
            table.put(args[0], args[1])
        elif op == "get":
            answer.append(table.get(args[0]))
        else:
            table.remove(args[0])
    return answer
