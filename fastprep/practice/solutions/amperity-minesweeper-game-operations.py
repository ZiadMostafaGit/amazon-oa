# Simulate the board with BFS flood fill over zero cells, emitting a snapshot per operation.
from typing import List, Optional, Any
from collections import deque


def playMinesweeper(rows: int, cols: int, mines: List[List[int]], operations: List[str]) -> List[str]:
    mine = [[False] * cols for _ in range(rows)]
    for r, c in mines:
        mine[r][c] = True

    adj = [[0] * cols for _ in range(rows)]
    for r in range(rows):
        for c in range(cols):
            if mine[r][c]:
                continue
            k = 0
            for dr in (-1, 0, 1):
                for dc in (-1, 0, 1):
                    if dr == 0 and dc == 0:
                        continue
                    nr, nc = r + dr, c + dc
                    if 0 <= nr < rows and 0 <= nc < cols and mine[nr][nc]:
                        k += 1
            adj[r][c] = k

    revealed = [[False] * cols for _ in range(rows)]
    total_safe = rows * cols - len(mines)
    opened_safe = 0
    status = "RUNNING"
    out = []

    def render():
        lines = []
        for r in range(rows):
            row = []
            for c in range(cols):
                if not revealed[r][c]:
                    row.append("#")
                elif mine[r][c]:
                    row.append("*")
                else:
                    row.append(str(adj[r][c]))
            lines.append("".join(row))
        return status + "|" + "/".join(lines)

    for op in operations:
        if status == "RUNNING":
            parts = op.split()
            r, c = int(parts[1]), int(parts[2])
            if not revealed[r][c]:
                if mine[r][c]:
                    revealed[r][c] = True
                    status = "LOST"
                else:
                    q = deque([(r, c)])
                    revealed[r][c] = True
                    opened_safe += 1
                    while q:
                        cr, cc = q.popleft()
                        if adj[cr][cc] != 0:
                            continue
                        for dr in (-1, 0, 1):
                            for dc in (-1, 0, 1):
                                if dr == 0 and dc == 0:
                                    continue
                                nr, nc = cr + dr, cc + dc
                                if 0 <= nr < rows and 0 <= nc < cols and not revealed[nr][nc] and not mine[nr][nc]:
                                    revealed[nr][nc] = True
                                    opened_safe += 1
                                    q.append((nr, nc))
                    if opened_safe == total_safe:
                        status = "WON"
        out.append(render())
    return out
