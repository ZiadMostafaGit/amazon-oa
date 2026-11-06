# One pass: if the running tank goes negative, no start up to here works; restart after it.
from typing import List, Optional, Any


def canCompleteCircuit(gas: List[int], cost: List[int]) -> int:
    total = 0
    tank = 0
    start = 0
    for i in range(len(gas)):
        d = gas[i] - cost[i]
        total += d
        tank += d
        if tank < 0:
            start = i + 1
            tank = 0
    return start if total >= 0 else -1
