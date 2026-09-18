# Simulation: hash map of handle -> object id plus a strong reference count per object.
from typing import List, Optional, Any


def simulateSharedPointer(operations: List[str]) -> List[str]:
    out: List[str] = []
    owner = {}          # handle name -> object id (absent/None means empty)
    counts = {}         # object id -> strong reference count
    order = []          # handles in order of first appearance
    seen = set()

    def touch(name: str) -> None:
        if name not in seen:
            seen.add(name)
            order.append(name)
            owner[name] = None

    def release(name: str) -> None:
        oid = owner.get(name)
        if oid is None:
            return
        owner[name] = None
        counts[oid] -= 1
        if counts[oid] == 0:
            del counts[oid]
            out.append("destroy:" + str(oid))

    for op in operations:
        parts = op.split()
        if not parts:
            continue
        cmd = parts[0]
        if cmd == "create":
            h, oid = parts[1], int(parts[2])
            touch(h)
            release(h)
            counts[oid] = 1
            owner[h] = oid
        elif cmd == "copy":
            tgt, src = parts[1], parts[2]
            touch(tgt)
            touch(src)
            if tgt == src:
                continue
            release(tgt)
            oid = owner.get(src)
            if oid is not None:
                counts[oid] += 1
                owner[tgt] = oid
        elif cmd == "move":
            tgt, src = parts[1], parts[2]
            touch(tgt)
            touch(src)
            if tgt == src:
                continue
            release(tgt)
            oid = owner.get(src)
            owner[src] = None
            owner[tgt] = oid
        elif cmd == "reset":
            h = parts[1]
            touch(h)
            release(h)
        elif cmd == "get":
            h = parts[1]
            touch(h)
            oid = owner.get(h)
            out.append("get:" + (str(oid) if oid is not None else "-1"))
        elif cmd == "use_count":
            h = parts[1]
            touch(h)
            oid = owner.get(h)
            out.append("use_count:" + str(counts[oid] if oid is not None else 0))

    for name in reversed(order):
        release(name)

    return out
