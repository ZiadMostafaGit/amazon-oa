# Hash map of content -> reference-counted physical block, bucketed by (length, ascii-sum hash) then exact compare.
from typing import List, Optional, Any


def processFileOperations(operations: List[List[str]]) -> List[List[str]]:
    # buckets: (length, mock_hash) -> list of block ids whose content matches that key
    buckets = {}
    # block id -> [content, refcount]
    blocks = {}
    next_id = [0]
    # logical path -> block id
    paths = {}

    def mock_hash(data: str) -> int:
        total = 0
        for ch in data:
            total += ord(ch)
        return total

    def release(bid: int) -> None:
        entry = blocks[bid]
        entry[1] -= 1
        if entry[1] == 0:
            content = entry[0]
            key = (len(content), mock_hash(content))
            lst = buckets.get(key)
            if lst is not None:
                for i, other in enumerate(lst):
                    if other == bid:
                        lst[i] = lst[-1]
                        lst.pop()
                        break
                if not lst:
                    del buckets[key]
            del blocks[bid]

    def acquire(data: str) -> bool:
        """Attach a reference to a block holding data. True if a new block was created."""
        key = (len(data), mock_hash(data))
        lst = buckets.get(key)
        if lst is not None:
            for bid in lst:
                if blocks[bid][0] == data:
                    blocks[bid][1] += 1
                    paths[path] = bid
                    return False
        else:
            lst = []
            buckets[key] = lst
        bid = next_id[0]
        next_id[0] += 1
        blocks[bid] = [data, 1]
        lst.append(bid)
        paths[path] = bid
        return True

    result = []
    for op in operations:
        cmd = op[0]
        if cmd == "WRITE":
            path = op[1]
            data = op[2]
            old = paths.pop(path, None)
            if old is not None:
                release(old)
            created = acquire(data)
            result.append(["true" if created else "false"])
        elif cmd == "READ":
            path = op[1]
            bid = paths.get(path)
            if bid is None:
                result.append([])
            else:
                result.append([blocks[bid][0]])
        else:  # DELETE
            path = op[1]
            bid = paths.pop(path, None)
            if bid is None:
                result.append(["false"])
            else:
                release(bid)
                result.append(["true"])
    return result
