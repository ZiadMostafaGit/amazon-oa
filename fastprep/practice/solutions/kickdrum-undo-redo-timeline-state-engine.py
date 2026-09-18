# Simulate a timeline as a list plus a cursor; DO truncates the redo branch.
from typing import List, Optional, Any


def runTimeline(initialState: str, operations: List[str]) -> List[str]:
    states = [initialState]
    cur = 0
    out = []
    for op in operations:
        parts = op.split(" ", 1)
        cmd = parts[0]
        if cmd == "DO":
            arg = parts[1].strip()
            del states[cur + 1:]
            states.append(arg)
            cur = len(states) - 1
        elif cmd == "UNDO":
            k = int(parts[1])
            cur = max(0, cur - k)
        elif cmd == "REDO":
            k = int(parts[1])
            cur = min(len(states) - 1, cur + k)
        # CURRENT: observe only
        out.append(states[cur])
    return out
