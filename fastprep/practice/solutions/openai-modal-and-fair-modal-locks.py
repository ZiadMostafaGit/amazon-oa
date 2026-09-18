# Direct simulation of two lock state machines (holder multiset + FIFO wait queue).
from typing import List, Optional, Any


def simulateModalLocks(compatibility: List[List[int]], operations: List[List[int]]) -> List[List[int]]:
    # per lock type: list of held modes (with thread ids), and a FIFO queue
    holders = [[], []]   # each entry: [threadId, mode]
    queues = [[], []]    # each entry: [threadId, mode]

    def compatible(lock: int, mode: int) -> bool:
        for _, held in holders[lock]:
            if compatibility[mode][held] != 1:
                return False
        return True

    def drain(lock: int) -> List[int]:
        granted = []
        q = queues[lock]
        while q:
            tid, mode = q[0]
            if not compatible(lock, mode):
                break
            q.pop(0)
            holders[lock].append((tid, mode))
            granted.append(tid)
        return granted

    result = []
    for op in operations:
        lock, action, tid, mode = op[0], op[1], op[2], op[3]
        row = []
        if action == 0:
            if lock == 0:
                ok = compatible(lock, mode)
            else:
                ok = (not queues[lock]) and compatible(lock, mode)
            if ok:
                holders[lock].append((tid, mode))
                row.append(tid)
            else:
                queues[lock].append((tid, mode))
        else:
            for i, (ht, hm) in enumerate(holders[lock]):
                if ht == tid and hm == mode:
                    holders[lock].pop(i)
                    break
            row = drain(lock)
        result.append(row)
    return result
