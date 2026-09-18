# Approach: index roles by name, then walk the parent chain returning the nearest explicit decision.
from typing import List, Optional, Any


def hasPermission(roles: List[str], parents: List[str], allowLists: List[List[str]], denyLists: List[List[str]], role: str, permission: str) -> bool:
    index = {name: i for i, name in enumerate(roles)}
    allows = [set(a) for a in allowLists]
    denies = [set(d) for d in denyLists]
    current = role
    seen = set()
    while current in index and current not in seen:
        seen.add(current)
        i = index[current]
        if permission in denies[i]:
            return False
        if permission in allows[i]:
            return True
        current = parents[i]
    return False
