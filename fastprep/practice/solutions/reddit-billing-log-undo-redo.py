# Linear history of states with a cursor: new edits truncate the redo tail.
from typing import List, Optional, Any


def billingStatusLog(operations: List[str], amounts: List[int]) -> List[int]:
    history = [0]
    ptr = 0
    out = []
    for op, amt in zip(operations, amounts):
        if op == "ADD" or op == "SET":
            nxt = history[ptr] + amt if op == "ADD" else amt
            del history[ptr + 1:]
            history.append(nxt)
            ptr += 1
        elif op == "UNDO":
            if ptr > 0:
                ptr -= 1
        elif op == "REDO":
            if ptr + 1 < len(history):
                ptr += 1
        out.append(history[ptr])
    return out
