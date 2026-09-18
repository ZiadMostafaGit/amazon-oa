# Simulation: per-seller priority buckets (FIFO deques) plus a round-robin deque with per-turn quotas.
from collections import deque
from typing import List, Optional, Any


def scheduleSellerTasks(operations: List[str], taskIds: List[str], sellerIds: List[str], sellerTiers: List[str], priorities: List[int]) -> List[str]:
    queues = {}     # sellerId -> [deque(p1), deque(p2), deque(p3)]
    quota = {}      # sellerId -> tasks allowed per turn
    active = set()  # sellers currently in the rotation
    rot = deque()
    used = 0        # tasks the current front seller has taken this turn
    out = []

    for idx, op in enumerate(operations):
        if op == "RECEIVE":
            sid = sellerIds[idx]
            q = queues.get(sid)
            if q is None:
                q = [deque(), deque(), deque()]
                queues[sid] = q
                quota[sid] = 2 if sellerTiers[idx] == "VIP" else 1
            q[priorities[idx] - 1].append(taskIds[idx])
            if sid not in active:
                active.add(sid)
                rot.append(sid)
        else:
            if not rot:
                out.append("")
                continue
            sid = rot[0]
            q = queues[sid]
            for bucket in q:
                if bucket:
                    tid = bucket.popleft()
                    break
            out.append(sid + ":" + tid)
            used += 1
            if not (q[0] or q[1] or q[2]):
                rot.popleft()
                active.discard(sid)
                used = 0
            elif used >= quota[sid]:
                rot.popleft()
                rot.append(sid)
                used = 0

    return out
