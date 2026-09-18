# Per-level max-heaps plus a global expiry min-heap, both with lazy deletion by serial.
import heapq
from typing import List


def processTieredStore(levelCapacities: List[int], operations: List[str]) -> List[str]:
    n_levels = len(levelCapacities)
    counts = [0] * n_levels
    level_heaps = [[] for _ in range(n_levels)]  # (-weight, id, serial)
    expiry_heap = []                             # (expiresAt, serial)
    live = {}                                    # serial -> (id, level)
    id_to_serial = {}
    serial = 0
    results = []

    def drop(s):
        item_id, level = live.pop(s)
        del id_to_serial[item_id]
        counts[level] -= 1

    for op in operations:
        parts = op.split()
        if parts[0] == "STORE":
            item_id, weight, expires_at = parts[1], int(parts[2]), int(parts[3])
            if item_id in id_to_serial:
                results.append("false")
                continue
            target = -1
            for lvl in range(n_levels):
                if counts[lvl] < levelCapacities[lvl]:
                    target = lvl
                    break
            if target < 0:
                results.append("false")
                continue
            serial += 1
            live[serial] = (item_id, target)
            id_to_serial[item_id] = serial
            counts[target] += 1
            heapq.heappush(level_heaps[target], (-weight, item_id, serial))
            heapq.heappush(expiry_heap, (expires_at, serial))
            results.append("true")
        else:
            now = int(parts[1])
            while expiry_heap and expiry_heap[0][0] <= now:
                _, s = heapq.heappop(expiry_heap)
                if s in live:
                    drop(s)
            chosen = "null"
            for lvl in range(n_levels):
                cap = levelCapacities[lvl]
                if counts[lvl] == 0 or 2 * (cap - counts[lvl]) < cap:
                    continue
                heap = level_heaps[lvl]
                while heap and heap[0][2] not in live:
                    heapq.heappop(heap)
                if not heap:
                    continue
                _, item_id, s = heapq.heappop(heap)
                drop(s)
                chosen = item_id
                break
            results.append(chosen)
    return results
