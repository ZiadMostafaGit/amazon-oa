# Approach: event simulation with a FIFO pending deque, an attempt counter per task and a min-heap of lease deadlines expired before each operation.
from typing import List, Optional, Any
from collections import deque
import heapq


def solve(operations: List[str], taskIds: List[str], timestamps: List[int], leaseDuration: int, maxAttempts: int) -> List[str]:
    pending = deque()          # task ids waiting to be reserved, in FIFO order
    attempts = {}              # task id -> reservations consumed so far
    active = {}                # task id -> current lease deadline
    deadline_heap = []         # (deadline, task id) for lazy expiry
    dead = set()               # dead-lettered task ids
    results = []

    def expire(now: int) -> None:
        while deadline_heap and deadline_heap[0][0] <= now:
            deadline, task = heapq.heappop(deadline_heap)
            if active.get(task) != deadline:
                continue       # stale entry: lease already released or renewed
            del active[task]
            if attempts.get(task, 0) >= maxAttempts:
                dead.add(task)
            else:
                pending.append(task)

    for i, op in enumerate(operations):
        task = taskIds[i] if i < len(taskIds) else ""
        now = timestamps[i]
        expire(now)

        if op == "ADD":
            if task in active or task in pending:
                results.append("EXISTS")
            else:
                dead.discard(task)
                attempts[task] = 0
                pending.append(task)
                results.append("ADDED")
        elif op == "RESERVE":
            if not pending:
                results.append("EMPTY")
            else:
                chosen = pending.popleft()
                attempts[chosen] = attempts.get(chosen, 0) + 1
                deadline = now + leaseDuration
                active[chosen] = deadline
                heapq.heappush(deadline_heap, (deadline, chosen))
                results.append(chosen)
        elif op == "FAIL":
            if task in active:
                del active[task]
                if attempts.get(task, 0) >= maxAttempts:
                    dead.add(task)
                    results.append("DEAD_LETTERED")
                else:
                    pending.append(task)
                    results.append("REQUEUED")
            else:
                results.append("IGNORED")
        elif op == "COMPLETE":
            if task in active:
                del active[task]
                attempts.pop(task, None)
                results.append("COMPLETED")
            else:
                results.append("IGNORED")
        else:
            results.append("IGNORED")

    return results
