# Iterative DFS from room 0 over the key graph, checking every room gets visited.
from typing import List, Optional, Any


def canVisitAllRooms(rooms: List[List[int]]) -> bool:
    n = len(rooms)
    seen = [False] * n
    seen[0] = True
    stack = [0]
    count = 1
    while stack:
        room = stack.pop()
        for key in rooms[room]:
            if not seen[key]:
                seen[key] = True
                count += 1
                stack.append(key)
    return count == n
