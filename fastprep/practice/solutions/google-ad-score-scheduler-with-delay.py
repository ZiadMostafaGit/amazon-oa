# Simulation with two heaps: a max-heap of eligible ads (lazy deletion) plus a
# min-heap of blocked ads keyed by the GET index at which they become eligible again.
from typing import List, Optional, Any
import heapq


def solve(operations: List[str]) -> List[str]:
    score = {}
    wait = {}
    eligible = []      # (-score, id) lazy max-heap
    blocked = []       # (available_at_get_index, id)
    live = set()       # ids currently represented in the eligible heap
    out = []
    t = 0              # index of the current GET call

    for op in operations:
        if op.startswith("INSERT"):
            _, ad_id, s, d = op.split()
            s = int(s)
            score[ad_id] = s
            wait[ad_id] = max(1, int(d))
            live.add(ad_id)
            heapq.heappush(eligible, (-s, ad_id))
            continue

        # GET
        while blocked and blocked[0][0] <= t:
            _, ad_id = heapq.heappop(blocked)
            live.add(ad_id)
            heapq.heappush(eligible, (-score[ad_id], ad_id))

        chosen = None
        while eligible:
            neg, ad_id = eligible[0]
            if ad_id in live and -neg == score[ad_id]:
                heapq.heappop(eligible)
                chosen = ad_id
                break
            heapq.heappop(eligible)

        if chosen is None:
            out.append("")
        else:
            out.append(chosen)
            score[chosen] -= 1
            live.discard(chosen)
            heapq.heappush(blocked, (t + wait[chosen] + 1, chosen))
        t += 1

    return out
