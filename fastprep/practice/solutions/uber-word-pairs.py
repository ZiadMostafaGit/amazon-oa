# Trie with two counters per node: words ending here, words passing through.
from typing import List, Optional, Any


def wordPairs(magics: List[str]) -> int:
    root = [{}, 0, 0]  # children, words ending here, words passing through (incl. ending)
    total = 0
    for w in magics:
        node = root
        for c in w:
            nxt = node[0].get(c)
            if nxt is None:
                nxt = node[0][c] = [{}, 0, 0]
            node = nxt
            total += node[1]          # earlier word that is a prefix of w (proper or equal)
        total += node[2] - node[1]    # earlier word that w is a proper prefix of
        # register w
        node = root
        for c in w:
            node = node[0][c]
            node[2] += 1
        node[1] += 1
    return total
