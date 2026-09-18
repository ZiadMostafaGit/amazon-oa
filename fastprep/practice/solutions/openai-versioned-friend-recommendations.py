# Persistent edge histories (per-edge sorted change log + binary search) plus a bounded top-k selection per query.
from typing import List, Dict
import bisect
import heapq


def _active_at(history, snap):
    # history: list of snapshot ids at which the edge toggled, starting from inactive.
    # An odd number of toggles at or before `snap` means the edge is active in that snapshot.
    idx = bisect.bisect_right(history, snap)
    return idx % 2 == 1


def recommendAtSnapshots(n: int, operations: List[str]) -> List[str]:
    adj: Dict[int, Dict[int, List[int]]] = {}
    snapshots = 0
    out: List[str] = []

    for op in operations:
        parts = op.split()
        cmd = parts[0]
        if cmd == "FOLLOW" or cmd == "UNFOLLOW":
            u = int(parts[1])
            v = int(parts[2])
            adj.setdefault(u, {}).setdefault(v, []).append(snapshots)
        elif cmd == "SNAPSHOT":
            out.append(str(snapshots))
            snapshots += 1
        elif cmd == "RECOMMEND":
            user = int(parts[1])
            snap = int(parts[2])
            k = int(parts[3])
            followed = set()
            for v, hist in adj.get(user, {}).items():
                if _active_at(hist, snap):
                    followed.add(v)
            scores: Dict[int, int] = {}
            for mid in followed:
                for cand, hist in adj.get(mid, {}).items():
                    if cand == user or cand in followed:
                        continue
                    if _active_at(hist, snap):
                        scores[cand] = scores.get(cand, 0) + 1
            # Bounded heap: keep the k best by (score desc, id asc).
            heap = []  # min-heap of (score, -cand) -> worst item on top
            for cand, sc in scores.items():
                if len(heap) < k:
                    heapq.heappush(heap, (sc, -cand))
                else:
                    if (sc, -cand) > heap[0]:
                        heapq.heapreplace(heap, (sc, -cand))
            best = sorted(heap, key=lambda x: (-x[0], -x[1]))
            ids = [str(-c) for _, c in best]
            out.append("[" + ",".join(ids) + "]")

    return out
