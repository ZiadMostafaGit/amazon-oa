# Direct step-by-step simulation of the cyclic command program with fuel bookkeeping.
from typing import List, Optional, Any


def cyclicProgramSteps(grid: List[str], program: str, initialFuel: int, refillAmount: int, maxSteps: int) -> int:
    rows = len(grid)
    cols = len(grid[0]) if rows else 0
    r = c = 0
    for i in range(rows):
        j = grid[i].find('S')
        if j != -1:
            r, c = i, j
            break
    if c == cols - 1:
        return 0

    moves = {'U': (-1, 0), 'D': (1, 0), 'L': (0, -1), 'R': (0, 1)}
    fuel = initialFuel
    n = len(program)
    for step in range(1, maxSteps + 1):
        cmd = program[(step - 1) % n]
        if cmd == 'F':
            if grid[r][c] != 'G':
                return -1
            fuel += refillAmount
        else:
            dr, dc = moves[cmd]
            nr, nc = r + dr, c + dc
            if nr < 0 or nr >= rows or nc < 0 or nc >= cols:
                return -1
            if grid[nr][nc] == '#':
                return -1
            if fuel <= 0:
                return -1
            fuel -= 1
            r, c = nr, nc
            if c == cols - 1:
                return step
    return -1
