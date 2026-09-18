# Hash map of pending sign-in timestamps per user; flag users whose paired session duration is within maxTime.
from typing import List, Optional, Any


def usersWithShortSession(logs: List[str], maxTime: int) -> List[str]:
    pending = {}
    good = set()
    for line in logs:
        parts = line.split()
        if len(parts) < 3:
            continue
        ts = int(parts[0])
        user = parts[1]
        action = parts[2]
        if action == "SIGNIN":
            pending[user] = ts
        elif action == "SIGNOUT":
            start = pending.pop(user, None)
            if start is not None and ts - start <= maxTime:
                good.add(user)
    return sorted(good)
