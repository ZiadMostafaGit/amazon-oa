# Explicit separate-chaining hash table: fixed bucket array of key/value node lists.
from typing import List, Optional, Any


class _Node:
    __slots__ = ("key", "val", "next")

    def __init__(self, key: int, val: int, nxt: Optional["_Node"]) -> None:
        self.key = key
        self.val = val
        self.next = nxt


class _HashMap:
    def __init__(self, capacity: int) -> None:
        self.capacity = capacity
        self.buckets: List[Optional[_Node]] = [None] * capacity

    def _index(self, key: int) -> int:
        return (key * 2654435761) % self.capacity

    def put(self, key: int, val: int) -> None:
        idx = self._index(key)
        node = self.buckets[idx]
        while node is not None:
            if node.key == key:
                node.val = val
                return
            node = node.next
        self.buckets[idx] = _Node(key, val, self.buckets[idx])

    def get(self, key: int) -> int:
        node = self.buckets[self._index(key)]
        while node is not None:
            if node.key == key:
                return node.val
            node = node.next
        return -1

    def remove(self, key: int) -> None:
        idx = self._index(key)
        node = self.buckets[idx]
        prev = None
        while node is not None:
            if node.key == key:
                if prev is None:
                    self.buckets[idx] = node.next
                else:
                    prev.next = node.next
                return
            prev = node
            node = node.next


def runHashMap(operations: List[str], keys: List[int], values: List[int]) -> List[int]:
    capacity = max(8, 2 * len(operations) + 1)
    table = _HashMap(capacity)
    out = []
    for i, op in enumerate(operations):
        if op == "put":
            table.put(keys[i], values[i])
        elif op == "get":
            out.append(table.get(keys[i]))
        elif op == "remove":
            table.remove(keys[i])
    return out
