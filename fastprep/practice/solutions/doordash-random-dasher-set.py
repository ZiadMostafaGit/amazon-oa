# Direct simulation of a dense array plus id->index map (swap-with-last on removal).
from typing import List, Optional, Any


def runRandomDasherSet(operations: List[str]) -> List[str]:
    arr: List[str] = []
    idx = {}
    out: List[str] = []
    for op in operations:
        parts = op.split(None, 1)
        cmd = parts[0]
        arg = parts[1].strip() if len(parts) > 1 else ""
        if cmd == "ADD":
            if arg in idx:
                out.append("false")
            else:
                idx[arg] = len(arr)
                arr.append(arg)
                out.append("true")
        elif cmd == "REMOVE":
            if arg not in idx:
                out.append("false")
            else:
                pos = idx.pop(arg)
                last = arr.pop()
                if pos < len(arr):
                    arr[pos] = last
                    idx[last] = pos
                out.append("true")
        else:  # PICK
            if not arr:
                out.append("null")
            else:
                draw = int(arg)
                out.append(arr[draw % len(arr)])
    return out
