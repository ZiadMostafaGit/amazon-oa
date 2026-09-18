# Stack simulation of cursor provenance (inserted vs original chars), then merge adjacent ops.
from typing import List, Optional, Any


def compressEditorActions(document: str, actions: List[List[str]]) -> List[List[str]]:
    ops = []          # entries: [kind, payload]; kind in {"I", "S", "D", "X"} (X = canceled)
    live = []         # indices of entries still present to the left of the cursor
    pos = 0           # how many original characters the cursor has passed

    for act in actions:
        kind = act[0]
        if kind == "APPEND":
            ops.append(["I", act[1]])
            live.append(len(ops) - 1)
        elif kind == "RIGHT":
            if pos < len(document):
                pos += 1
                ops.append(["S", 1])
                live.append(len(ops) - 1)
        else:  # BACKSPACE
            if not live:
                continue
            idx = live.pop()
            if ops[idx][0] == "I":
                ops[idx][0] = "X"
            else:
                ops[idx][0] = "D"

    out = []
    for kind, payload in ops:
        if kind == "X":
            continue
        name = "INSERT" if kind == "I" else ("DELETE" if kind == "D" else "SKIP")
        if out and out[-1][0] == name:
            if name == "INSERT":
                out[-1][1] += payload
            else:
                out[-1][1] += 1
        else:
            out.append([name, payload if name == "INSERT" else 1])

    return [[name, val if name == "INSERT" else str(val)] for name, val in out]
