# Address-ordered first-fit free list with splitting on allocate and coalescing on free.
from typing import List, Optional, Any
import bisect


def runAllocator(totalBytes: int, alignment: int, operations: List[str], values: List[int]) -> List[int]:
    # free ranges kept address-ordered and maximal: starts[i] .. starts[i]+sizes[i]
    starts = [0]
    sizes = [totalBytes]
    live = {}  # start address -> rounded size
    out = []

    for op, v in zip(operations, values):
        if op == "allocate":
            need = ((v + alignment - 1) // alignment) * alignment
            idx = -1
            for i, s in enumerate(sizes):
                if s >= need:
                    idx = i
                    break
            if idx == -1:
                out.append(-1)
                continue
            addr = starts[idx]
            if sizes[idx] == need:
                del starts[idx]
                del sizes[idx]
            else:
                starts[idx] = addr + need
                sizes[idx] -= need
            live[addr] = need
            out.append(addr)
        else:
            addr = v
            size = live.pop(addr)
            i = bisect.bisect_left(starts, addr)
            # merge with the following free range when adjacent
            if i < len(starts) and addr + size == starts[i]:
                size += sizes[i]
                del starts[i]
                del sizes[i]
            # merge with the preceding free range when adjacent
            if i > 0 and starts[i - 1] + sizes[i - 1] == addr:
                sizes[i - 1] += size
            else:
                starts.insert(i, addr)
                sizes.insert(i, size)
    return out
