# Simulate on a deque of alternating run-length color blocks; a flip merges at most two end blocks.
from collections import deque
from typing import List, Optional, Any


def countTiles(s: str) -> List[int]:
    # color 0 = black, 1 = white; board starts as one black tile then one white tile
    blocks = deque([[0, 1], [1, 1]])
    for i, ch in enumerate(s):
        color = 0 if (i + 1) % 2 == 1 else 1
        if ch == 'L':
            if blocks[0][0] == color:
                blocks[0][1] += 1
            elif len(blocks) >= 2:
                a = blocks.popleft()
                b = blocks.popleft()
                blocks.appendleft([color, a[1] + b[1] + 1])
            else:
                blocks.appendleft([color, 1])
        else:
            if blocks[-1][0] == color:
                blocks[-1][1] += 1
            elif len(blocks) >= 2:
                a = blocks.pop()
                b = blocks.pop()
                blocks.append([color, a[1] + b[1] + 1])
            else:
                blocks.append([color, 1])
    black = sum(c for col, c in blocks if col == 0)
    white = sum(c for col, c in blocks if col == 1)
    return [black, white]
