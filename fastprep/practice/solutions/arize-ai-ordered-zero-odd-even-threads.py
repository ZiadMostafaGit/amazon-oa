# Three real threads sharing a monotonically increasing counter guarded by a Condition variable.
import threading
from typing import List, Optional, Any


def orderedThreadOutput(n: int, startOrder: List[int]) -> List[str]:
    lock = threading.Lock()
    cond = threading.Condition(lock)
    state = [0]          # the next value that is allowed to be emitted
    log: List[str] = []

    def worker(name: str, values: List[int]) -> None:
        for v in values:
            with cond:
                while state[0] != v:
                    cond.wait()
                log.append(name + ":" + str(v))
                state[0] += 1
                cond.notify_all()

    zero_vals = [0]
    odd_vals = list(range(1, n + 1, 2))
    even_vals = list(range(2, n + 1, 2))

    threads = {
        0: threading.Thread(target=worker, args=("ZeroThread", zero_vals)),
        1: threading.Thread(target=worker, args=("OddThread", odd_vals)),
        2: threading.Thread(target=worker, args=("EvenThread", even_vals)),
    }

    for role in startOrder:
        threads[role].start()
    for role in (0, 1, 2):
        threads[role].join()

    return log
