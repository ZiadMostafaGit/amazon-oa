# Keep rectangles in draw order (layer order) and repaint the canvas bottom-up at the end.
from typing import List, Optional, Any


def renderRectangleCanvas(rows: int, cols: int, commands: List[str]) -> List[str]:
    order = []          # ids in draw order = bottom-to-top layer order
    rects = {}          # id -> [top, left, height, width, ch]
    for cmd in commands:
        parts = cmd.split()
        op = parts[0]
        if op == "DRAW":
            rid = parts[1]
            top = int(parts[2])
            left = int(parts[3])
            height = int(parts[4])
            width = int(parts[5])
            ch = parts[6]
            rects[rid] = [top, left, height, width, ch]
            order.append(rid)
        elif op == "MOVE":
            rid = parts[1]
            r = rects[rid]
            r[0] += int(parts[2])
            r[1] += int(parts[3])

    grid = [['.'] * cols for _ in range(rows)]
    for rid in order:
        top, left, height, width, ch = rects[rid]
        for r in range(top, top + height):
            if 0 <= r < rows:
                row = grid[r]
                for c in range(left, left + width):
                    if 0 <= c < cols:
                        row[c] = ch
    return [''.join(row) for row in grid]
