# Simulation: keep lines as char lists with a (row, col) cursor and apply each operation.
from typing import List, Optional, Any


def runCursorEditor(operations: List[List[str]]) -> List[List[str]]:
    lines = [[]]
    row = 0
    col = 0
    out = []
    for op in operations:
        kind = op[0]
        if kind == "INSERT":
            text = op[1]
            lines[row][col:col] = list(text)
            col += len(text)
        elif kind == "BACKSPACE":
            if col > 0:
                del lines[row][col - 1]
                col -= 1
            elif row > 0:
                cur = lines.pop(row)
                row -= 1
                col = len(lines[row])
                lines[row].extend(cur)
        elif kind == "NEWLINE":
            suffix = lines[row][col:]
            del lines[row][col:]
            lines.insert(row + 1, suffix)
            row += 1
            col = 0
        elif kind == "LEFT":
            if col > 0:
                col -= 1
            elif row > 0:
                row -= 1
                col = len(lines[row])
        elif kind == "RIGHT":
            if col < len(lines[row]):
                col += 1
            elif row < len(lines) - 1:
                row += 1
                col = 0
        elif kind == "UP":
            if row > 0:
                row -= 1
                col = min(col, len(lines[row]))
        elif kind == "DOWN":
            if row < len(lines) - 1:
                row += 1
                col = min(col, len(lines[row]))
        elif kind == "PRINT":
            out.append(["".join(ln) for ln in lines])
    return out
