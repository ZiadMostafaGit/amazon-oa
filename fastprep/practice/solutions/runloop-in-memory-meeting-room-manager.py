# Approach: per-room sorted interval list with binary search on start times for neighbour overlap checks, plus an id -> reservation map.
from typing import List, Optional, Any, Dict, Tuple
import bisect


def processMeetingRoomOperations(operations: List[str]) -> List[bool]:
    rooms: Dict[str, Tuple[List[int], List[int]]] = {}
    active: Dict[str, Tuple[str, int, int]] = {}
    res: List[bool] = []

    for op in operations:
        parts = op.split(" ")
        if parts[0] == "RESERVE":
            rid, room = parts[1], parts[2]
            start, end = int(parts[3]), int(parts[4])
            if rid in active:
                res.append(False)
                continue
            starts, ends = rooms.setdefault(room, ([], []))
            i = bisect.bisect_right(starts, start)
            ok = True
            if i > 0 and ends[i - 1] > start:
                ok = False
            elif i < len(starts) and starts[i] < end:
                ok = False
            if not ok:
                res.append(False)
                continue
            starts.insert(i, start)
            ends.insert(i, end)
            active[rid] = (room, start, end)
            res.append(True)
        else:
            rid = parts[1]
            info = active.pop(rid, None)
            if info is None:
                res.append(False)
                continue
            room, start, end = info
            starts, ends = rooms[room]
            i = bisect.bisect_left(starts, start)
            del starts[i]
            del ends[i]
            res.append(True)
    return res
