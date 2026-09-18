# Forward BFS over the bounded grid, pruning coordinates past the target and perfect-square sums.
from collections import deque
from math import isqrt


def _forbidden(s: int) -> bool:
    r = isqrt(s)
    return r * r == s


def canReach(c: int, startX: int, startY: int, targetX: int, targetY: int) -> str:
    if _forbidden(startX + startY) or _forbidden(targetX + targetY):
        return "No"
    if startX > targetX or startY > targetY:
        return "No"
    if startX == targetX and startY == targetY:
        return "Yes"
    seen = {(startX, startY)}
    q = deque([(startX, startY)])
    while q:
        x, y = q.popleft()
        for nx, ny in ((x + y, y), (x, x + y), (x + c, y + c)):
            if nx > targetX or ny > targetY:
                continue
            if (nx, ny) in seen:
                continue
            if _forbidden(nx + ny):
                continue
            if nx == targetX and ny == targetY:
                return "Yes"
            seen.add((nx, ny))
            q.append((nx, ny))
    return "No"
