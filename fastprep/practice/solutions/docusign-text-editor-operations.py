# Simulation with a two-stack (gap buffer) cursor model.
from typing import List, Optional, Any


def getPrintedStrings(commands: List[List[str]]) -> List[str]:
    left: List[str] = []   # characters before the cursor (in order)
    right: List[str] = []  # characters after the cursor, reversed
    out: List[str] = []

    for cmd in commands:
        op = str(cmd[0]).strip().upper()
        arg = cmd[1] if len(cmd) > 1 else ""
        if op == "INSERT":
            left.extend(str(arg))
        elif op == "LEFT":
            k = min(int(arg), len(left))
            for _ in range(k):
                right.append(left.pop())
        elif op == "RIGHT":
            k = min(int(arg), len(right))
            for _ in range(k):
                left.append(right.pop())
        elif op == "BACKSPACE":
            k = min(int(arg), len(left))
            for _ in range(k):
                left.pop()
        elif op == "DELETE":
            k = min(int(arg), len(right))
            for _ in range(k):
                right.pop()
        elif op == "PRINT":
            x = int(arg)
            cur = len(left)
            n = cur + len(right)
            lo = max(0, cur - x)
            hi = min(n - 1, cur + x)
            if hi < lo:
                out.append("")
            else:
                doc = left + right[::-1]
                out.append("".join(doc[lo:hi + 1]))
    return out
