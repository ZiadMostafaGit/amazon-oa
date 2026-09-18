# Single pass accumulating unit deltas from a case-insensitive direction table.
from typing import List, Optional, Any

_DELTA = {"l": (-1, 0), "r": (1, 0), "u": (0, 1), "d": (0, -1)}


def finalCoordinates(commands: str) -> List[int]:
    x = y = 0
    for ch in commands or "":
        move = _DELTA.get(ch.lower())
        if move is not None:
            x += move[0]
            y += move[1]
    return [x, y]
