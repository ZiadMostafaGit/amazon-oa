# Simulate the partition as a list of part lengths, re-checking the maximum after each operation.
from typing import List, Optional, Any


def classifyParts(initialParts: List[str], operations: List[List[str]], maxPartLength: int) -> List[str]:
    lengths = [len(p) for p in initialParts]
    out = []
    for op in operations:
        kind = op[0]
        i = int(op[1])
        if kind == "SPLIT":
            offset = int(op[2])
            total = lengths[i]
            lengths[i:i + 1] = [offset, total - offset]
        else:
            merged = lengths[i] + lengths[i + 1]
            lengths[i:i + 2] = [merged]
        out.append("QUALIFIED" if max(lengths) <= maxPartLength else "UNQUALIFIED")
    return out
