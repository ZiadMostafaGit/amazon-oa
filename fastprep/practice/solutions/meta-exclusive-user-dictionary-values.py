# Set difference between the current user's values and the union of all other rows.
from typing import List, Optional, Any


def exclusiveValues(userValues: List[List[str]], currentUser: int) -> List[str]:
    others = set()
    for i, row in enumerate(userValues):
        if i != currentUser:
            others.update(row)
    mine = set(userValues[currentUser])
    return sorted(mine - others)
