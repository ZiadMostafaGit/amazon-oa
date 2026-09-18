# Stack of tagged nodes plus a lazy max-heap keyed by (-value, -id) so ties favor the topmost node.
import heapq
from typing import List, Optional, Any


def runMaxStack(operations: List[str]) -> List[int]:
    stack = []          # list of ids in push order
    vals = {}           # id -> value
    alive = set()
    heap = []           # (-value, -id)
    out = []
    next_id = 0

    def top_id():
        while stack and stack[-1] not in alive:
            stack.pop()
        return stack[-1] if stack else None

    def max_entry():
        while heap and -heap[0][1] not in alive:
            heapq.heappop(heap)
        return heap[0] if heap else None

    for op in operations:
        if op.startswith("PUSH"):
            v = int(op[5:])
            nid = next_id
            next_id += 1
            vals[nid] = v
            alive.add(nid)
            stack.append(nid)
            heapq.heappush(heap, (-v, -nid))
        elif op == "POP":
            nid = top_id()
            stack.pop()
            alive.discard(nid)
            out.append(vals[nid])
        elif op == "PEEK":
            out.append(vals[top_id()])
        elif op == "PEEK_MAX":
            out.append(-max_entry()[0])
        elif op == "POP_MAX":
            nv, nid = heapq.heappop(heap) if max_entry() else (None, None)
            nid = -nid
            alive.discard(nid)
            out.append(-nv)
    return out
