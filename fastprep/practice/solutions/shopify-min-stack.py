# Each stack entry stores (value, minimum of the stack up to and including it). O(1) per op.
from typing import List, Optional, Any


def runMinStack(operations: List[str], values: List[int]) -> List[int]:
    st = []
    out = []
    for op, v in zip(operations, values):
        if op == "push":
            st.append((v, v if not st or v < st[-1][1] else st[-1][1]))
        elif op == "pop":
            st.pop()
        elif op == "top":
            out.append(st[-1][0])
        else:
            out.append(st[-1][1])
    return out
