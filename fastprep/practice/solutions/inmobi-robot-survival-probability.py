# Forward DP over the grid, spreading each cell's probability to its four neighbours.
def robotSurvivalProbability(rows: int, cols: int, startRow: int, startCol: int, steps: int) -> float:
    cur = [[0.0] * cols for _ in range(rows)]
    cur[startRow][startCol] = 1.0
    for _ in range(steps):
        nxt = [[0.0] * cols for _ in range(rows)]
        for r in range(rows):
            row = cur[r]
            for c in range(cols):
                p = row[c]
                if p == 0.0:
                    continue
                q = p / 4.0
                if r > 0:
                    nxt[r - 1][c] += q
                if r + 1 < rows:
                    nxt[r + 1][c] += q
                if c > 0:
                    nxt[r][c - 1] += q
                if c + 1 < cols:
                    nxt[r][c + 1] += q
        cur = nxt
    return sum(sum(row) for row in cur)
