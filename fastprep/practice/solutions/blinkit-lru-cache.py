# LRU cache built from a hash map plus a doubly linked list of recency.
from typing import List, Optional, Any


def runLRU(capacity: int, operations: List[str]) -> List[int]:
    head = ['head', None, None, None]   # [key, value, prev, next]
    tail = ['tail', None, None, None]
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

    out = []
    for op in operations:
        parts = op.split()
        if parts[0] == 'GET':
            key = int(parts[1])
            node = table.get(key)
            if node is None:
                out.append(-1)
            else:
                unlink(node)
                push_front(node)
                out.append(node[1])
        else:
            key = int(parts[1])
            value = int(parts[2])
            node = table.get(key)
            if node is not None:
                node[1] = value
                unlink(node)
                push_front(node)
            else:
                if len(table) >= capacity:
                    lru = tail[2]
                    if lru is not head:
                        unlink(lru)
                        del table[lru[0]]
                node = [key, value, None, None]
                table[key] = node
                push_front(node)
    return out
