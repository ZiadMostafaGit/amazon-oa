# Trie of the word list plus backtracking DFS from every cell, pruning exhausted trie branches.
from typing import List, Optional, Any


def solve(board: List[List[str]], words: List[str]) -> List[str]:
    if not board or not board[0]:
        return []
    root = {}
    for w in words:
        node = root
        for ch in w:
            node = node.setdefault(ch, {})
        node["$"] = w

    rows, cols = len(board), len(board[0])
    found = []

    def dfs(i: int, j: int, node: dict) -> None:
        ch = board[i][j]
        nxt = node.get(ch)
        if nxt is None:
            return
        word = nxt.pop("$", None)
        if word is not None:
            found.append(word)
        board[i][j] = "#"
        for di, dj in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            ni, nj = i + di, j + dj
            if 0 <= ni < rows and 0 <= nj < cols and board[ni][nj] != "#":
                dfs(ni, nj, nxt)
        board[i][j] = ch
        if not nxt:
            node.pop(ch, None)

    for i in range(rows):
        for j in range(cols):
            dfs(i, j, root)
    return found
