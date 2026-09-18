# DP over k steps of the probability of still being on the board; the answer is one minus that.
def knightExitProbability(n: int, k: int, row: int, column: int) -> float:
    moves = ((1, 2), (2, 1), (2, -1), (1, -2), (-1, -2), (-2, -1), (-2, 1), (-1, 2))
    cur = [[0.0] * n for _ in range(n)]
    cur[row][column] = 1.0
    for _ in range(k):
        nxt = [[0.0] * n for _ in range(n)]
        for r in range(n):
            crow = cur[r]
            for c in range(n):
                p = crow[c]
                if p == 0.0:
                    continue
                p8 = p / 8.0
                for dr, dc in moves:
                    nr, nc = r + dr, c + dc
                    if 0 <= nr < n and 0 <= nc < n:
                        nxt[nr][nc] += p8
        cur = nxt
    survive = sum(sum(r) for r in cur)
    return 1.0 - survive
