# Event-driven simulation: jump directly to the next shutdown second using linear temperature rates.
from typing import List, Optional, Any


def simulateOverheatController(pooledCooling: int, coreIds: List[int], activeCooling: List[int], shutdownTemperature: int, operations: List[str], operationData: List[List[int]]) -> List[List[int]]:
    n = len(coreIds)
    pos = {cid: i for i, cid in enumerate(coreIds)}
    load = [0] * n
    temp = [0] * n
    running = [True] * n
    changed = set()
    state = {"time": 0}
    S = shutdownTemperature

    def advance(target: int) -> None:
        remaining = target - state["time"]
        if remaining < 0:
            remaining = 0
        state["time"] = max(state["time"], target)
        while remaining > 0:
            idxs = [i for i in range(n) if running[i]]
            r = len(idxs)
            if r == 0:
                break
            pc = pooledCooling // r
            deltas = [load[i] - activeCooling[i] - pc for i in idxs]
            k = remaining
            for j, i in enumerate(idxs):
                d = deltas[j]
                if d > 0:
                    need = S - temp[i]
                    steps = -(-need // d)
                    if steps < k:
                        k = steps
            for j, i in enumerate(idxs):
                t = temp[i] + k * deltas[j]
                temp[i] = t if t > 0 else 0
            remaining -= k
            stopped = False
            for i in idxs:
                if temp[i] >= S:
                    running[i] = False
                    changed.add(coreIds[i])
                    stopped = True
            if not stopped and k == 0:
                break

    result: List[List[int]] = []
    for op, data in zip(operations, operationData):
        if op == "SetCoreLoad":
            ts, cid, watts = data[0], data[1], data[2]
            advance(ts)
            i = pos[cid]
            load[i] = watts
            if not running[i]:
                running[i] = True
                temp[i] = 0
                changed.add(cid)
        else:
            advance(data[0])
            result.append(sorted(changed))
            changed.clear()
    return result
