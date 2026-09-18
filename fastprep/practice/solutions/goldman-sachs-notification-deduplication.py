# OrderedDict as an LRU-by-last-seen window; evict ids whose last sighting fell out of 600s.
from collections import OrderedDict
from typing import List

WINDOW = 600


def deduplicateNotifications(notificationIds: List[str], timestamps: List[int]) -> List[bool]:
    active = OrderedDict()
    out = []
    for nid, ts in zip(notificationIds, timestamps):
        while active:
            oldest_id, oldest_ts = next(iter(active.items()))
            if ts - oldest_ts >= WINDOW:
                active.popitem(last=False)
            else:
                break
        prev = active.get(nid)
        if prev is None or ts - prev >= WINDOW:
            out.append(True)
        else:
            out.append(False)
        active[nid] = ts
        active.move_to_end(nid)
    return out
