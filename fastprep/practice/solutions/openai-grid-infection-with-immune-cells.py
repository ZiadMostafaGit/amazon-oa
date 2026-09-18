# Frontier simulation with immune cells: counts track infected neighbors, 'I' never infects or is infected.
from typing import List, Optional, Any


def solveGridInfectionWithImmuneCells(input: str) -> List[str]:
    tokens = input.split("\n")
    idx = 0
    while idx < len(tokens) and tokens[idx].strip() == "":
        idx += 1
    header = tokens[idx].split()
    m = int(header[0])
    n = int(header[1])
    idx += 1
    if len(header) >= 3:
        t = int(header[2])
    else:
        while tokens[idx].strip() == "":
            idx += 1
        t = int(tokens[idx].strip())
        idx += 1

    grid = []
    while len(grid) < m and idx < len(tokens):
        row = tokens[idx].rstrip("\r")
        idx += 1
        if row.strip() == "" and len(row) < n:
            continue
        grid.append(list(row))

    for r in grid:
        while len(r) < n:
            r.append(".")

    dirs = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]

    counts = [[0] * n for _ in range(m)]
    for i in range(m):
        for j in range(n):
            if grid[i][j] == 'X':
                for di, dj in dirs:
                    a, b = i + di, j + dj
                    if 0 <= a < m and 0 <= b < n:
                        counts[a][b] += 1

    candidates = set()
    for i in range(m):
        for j in range(n):
            if grid[i][j] == '.':
                candidates.add((i, j))

    days = 0
    while candidates:
        newly = [(i, j) for (i, j) in candidates if grid[i][j] == '.' and counts[i][j] >= t]
        if not newly:
            break
        days += 1
        for i, j in newly:
            grid[i][j] = 'X'
        nxt = set()
        for i, j in newly:
            for di, dj in dirs:
                a, b = i + di, j + dj
                if 0 <= a < m and 0 <= b < n:
                    counts[a][b] += 1
                    if grid[a][b] == '.':
                        nxt.add((a, b))
        candidates = nxt

    return [str(days)]
