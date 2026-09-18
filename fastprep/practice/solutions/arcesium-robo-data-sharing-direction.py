# Closed-form snake traversal: rows are swept alternately, so only the row's last cell turns.
def nextDataDirection(rows: int, cols: int, startRow: int, startCol: int, row: int, col: int) -> str:
    # Initial horizontal sweep direction: +1 means rightward, -1 means leftward.
    hdir0 = 1 if startCol == 1 else -1
    # Vertical progression: +1 means downward (started at the top), -1 means upward.
    vdir = 1 if startRow == 1 else -1

    # How many rows have been traversed before reaching this one.
    band = (row - startRow) * vdir
    hdir = hdir0 if band % 2 == 0 else -hdir0

    last_col = cols if hdir == 1 else 1
    if col != last_col:
        return "Right" if hdir == 1 else "Left"

    # End of this row: either drop to the next row, or the traversal is finished.
    if band == rows - 1:
        return "Over"
    return "Back" if vdir == 1 else "Front"
