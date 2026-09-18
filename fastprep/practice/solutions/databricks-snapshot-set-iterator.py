# Insertion-ordered dict for the set; each ITERATOR copies the current key order as a snapshot.
from typing import List, Optional, Any


def runSnapshotSet(operations: List[List[str]]) -> List[str]:
    values = {}
    iterators = {}
    out: List[str] = []
    for op in operations:
        name = op[0]
        arg = op[1] if len(op) > 1 else None
        if name == "ADD":
            if arg not in values:
                values[arg] = True
        elif name == "REMOVE":
            if arg in values:
                del values[arg]
        elif name == "ITERATOR":
            iterators[arg] = [list(values.keys()), 0]
        elif name == "NEXT":
            it = iterators.get(arg)
            if it is None or it[1] >= len(it[0]):
                out.append("<END>")
            else:
                out.append(it[0][it[1]])
                it[1] += 1
    return out
