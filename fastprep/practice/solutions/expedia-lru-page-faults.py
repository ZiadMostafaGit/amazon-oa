# LRU cache: a hash map from page to node plus a doubly linked list in recency order (head = least recent).
from typing import List


class _Node:
    __slots__ = ("key", "prev", "next")

    def __init__(self, key=None):
        self.key = key
        self.prev = self.next = None


def lruFaults(pages: List[int], capacity: int) -> int:
    if capacity <= 0:
        return len(pages)
    head, tail = _Node(), _Node()      # sentinels: head.next is the LRU page, tail.prev the MRU page
    head.next, tail.prev = tail, head
    where = {}

    def unlink(node):
        node.prev.next = node.next
        node.next.prev = node.prev

    def push_back(node):
        node.prev, node.next = tail.prev, tail
        tail.prev.next = node
        tail.prev = node

    faults = 0
    for p in pages:
        node = where.get(p)
        if node is not None:
            unlink(node)
            push_back(node)
            continue
        faults += 1
        if len(where) == capacity:
            lru = head.next
            unlink(lru)
            del where[lru.key]
        node = _Node(p)
        where[p] = node
        push_back(node)
    return faults
