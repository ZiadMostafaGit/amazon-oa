# Per-user fixed-window counters keyed by UTC hour and day bucket; reject without mutating state.
from typing import List, Optional, Any


def applyRateLimits(userIds: List[str], efforts: List[int], timestamps: List[int], hourlyLimit: int, dailyLimit: int) -> List[bool]:
    hour_used = {}
    day_used = {}
    result = []
    for uid, eff, ts in zip(userIds, efforts, timestamps):
        hkey = (uid, ts // 3600)
        dkey = (uid, ts // 86400)
        h = hour_used.get(hkey, 0)
        d = day_used.get(dkey, 0)
        if h + eff <= hourlyLimit and d + eff <= dailyLimit:
            hour_used[hkey] = h + eff
            day_used[dkey] = d + eff
            result.append(True)
        else:
            result.append(False)
    return result
