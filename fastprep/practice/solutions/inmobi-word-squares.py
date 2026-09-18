# Backtracking with a prefix->words trie/dict index, building rows one at a time.
from typing import List, Optional, Any
from collections import defaultdict


def findWordSquares(words: List[str]) -> List[List[str]]:
    if not words:
        return []
    n = len(words[0])
    words = sorted(words)
    prefix_map = defaultdict(list)
    for w in words:
        for i in range(len(w) + 1):
            prefix_map[w[:i]].append(w)

    result = []
    square = []

    def backtrack(row: int) -> None:
        if row == n:
            result.append(list(square))
            return
        prefix = ''.join(square[k][row] for k in range(row))
        for cand in prefix_map.get(prefix, ()):
            square.append(cand)
            backtrack(row + 1)
            square.pop()

    backtrack(0)
    return result
