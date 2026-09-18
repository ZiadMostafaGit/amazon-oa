# Hash map of nodes plus a doubly linked list giving O(1) get/put with LRU eviction.
from typing import List, Optional, Any


def runLRU(capacity: int, operations: List[str]) -> List[int]:
    # node = [key, value, prev, next]
    head: List[Any] = [None, None, None, None]  # most-recent sentinel
    tail: List[Any] = [None, None, None, None]  # least-recent sentinel
    head[3] = tail
    tail[2] = head
    table = {}

    def unlink(node):
        node[2][3] = node[3]
        node[3][2] = node[2]

    def push_front(node):
        nxt = head[3]
        node[2] = head
        node[3] = nxt
        head[3] = node
        nxt[2] = node

    out: List[int] = []
    for op in operations:
        parts = op.split()
        if parts[0] == "PUT":
            key = int(parts[1])
            val = int(parts[2])
            node = table.get(key)
            if node is not None:
                node[1] = val
                unlink(node)
                push_front(node)
            else:
                if len(table) >= capacity:
                    lru = tail[2]
                    unlink(lru)
                    del table[lru[0]]
                node = [key, val, None, None]
                table[key] = node
                push_front(node)
        else:
            key = int(parts[1])
            node = table.get(key)
            if node is None:
                out.append(-1)
            else:
                out.append(node[1])
                unlink(node)
                push_front(node)
    return out
