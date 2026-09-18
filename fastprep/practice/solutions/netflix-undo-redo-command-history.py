# Two stacks: active history and a redo stack cleared on each new EXECUTE.
from typing import List, Optional, Any


def runUndoRedoHistory(operations: List[List[str]]) -> List[str]:
    active = []
    redo = []
    out = []
    for op in operations:
        kind = op[0]
        if kind == "EXECUTE":
            active.append(op[1])
            redo.clear()
        elif kind == "UNDO":
            if active:
                redo.append(active.pop())
        else:  # REDO
            if redo:
                active.append(redo.pop())
        out.append("|".join(active))
    return out
