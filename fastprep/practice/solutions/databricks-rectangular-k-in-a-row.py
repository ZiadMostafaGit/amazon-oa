# Sparse hash-map board with O(1) run merging: each new mark joins the runs at its two endpoints in all 4 directions.
from typing import List, Dict, Tuple


def playKInARow(rows: int, columns: int, k: int, moves: List[List[int]]) -> List[int]:
    owner: Dict[Tuple[int, int], int] = {}
    dirs = ((0, 1), (1, 0), (1, 1), (1, -1))
    runs: List[Dict[Tuple[int, int], int]] = [{} for _ in dirs]
    res: List[int] = []
    won = False

    for row, col, player in moves:
        if won:
            res.append(0)
            continue
        owner[(row, col)] = player
        win = False
        for di, (dr, dc) in enumerate(dirs):
            table = runs[di]
            back = (row - dr, col - dc)
            fwd = (row + dr, col + dc)
            left = table.get(back, 0) if owner.get(back) == player else 0
            right = table.get(fwd, 0) if owner.get(fwd) == player else 0
            total = left + right + 1
            table[(row, col)] = total
            if left:
                table[(row - dr * left, col - dc * left)] = total
            if right:
                table[(row + dr * right, col + dc * right)] = total
            if total >= k:
                win = True
        if win:
            won = True
            res.append(player)
        else:
            res.append(0)

    return res
