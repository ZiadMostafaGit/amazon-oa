# Sliding-window deques: one per element plus a global one, evicting hits outside (q-300, q].
from typing import List, Optional, Any
from collections import deque, defaultdict


def processHitCounterCommands(commands: List[str]) -> List[int]:
    WINDOW = 300
    per = defaultdict(deque)
    total = deque()
    out: List[int] = []
    for cmd in commands:
        parts = cmd.split()
        kind = parts[0]
        if kind == "HIT":
            el = parts[1]
            t = int(parts[2])
            per[el].append(t)
            total.append(t)
        elif kind == "GET":
            el = parts[1]
            q = int(parts[2])
            dq = per[el]
            while dq and dq[0] <= q - WINDOW:
                dq.popleft()
            out.append(len(dq))
        else:
            q = int(parts[1])
            while total and total[0] <= q - WINDOW:
                total.popleft()
            out.append(len(total))
    return out
