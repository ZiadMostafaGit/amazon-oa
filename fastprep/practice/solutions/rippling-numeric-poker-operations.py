# Rank hands by (category, right-to-left key); complete prefixes by enumerating fill multisets with their optimal arrangement.
from typing import List, Optional, Any
from itertools import combinations_with_replacement
from collections import Counter

DIGITS = "123456789"

# counts shape -> category index (0 = strongest)
_SHAPE = {
    (5,): 0,
    (4, 1): 1,
    (3, 2): 2,
    (2, 2, 1): 3,
    (3, 1, 1): 4,
    (2, 1, 1, 1): 5,
    (1, 1, 1, 1, 1): 6,
}


def _category(hand: str) -> int:
    shape = tuple(sorted(Counter(hand).values(), reverse=True))
    return _SHAPE[shape]


def _key(hand: str):
    # smaller category is stronger; among equal categories a larger reversed string is stronger
    return (-_category(hand), hand[::-1])


def processNumericPokerOperations(operations: List[List[str]]) -> List[str]:
    best_cache = {}
    worst_cache = {}

    def complete(partial: str, want_best: bool) -> str:
        cache = best_cache if want_best else worst_cache
        if partial in cache:
            return cache[partial]
        k = 5 - len(partial)
        if k <= 0:
            cache[partial] = partial
            return partial
        chosen = None
        chosen_key = None
        for combo in combinations_with_replacement(DIGITS, k):
            # combo is ascending; ascending left-to-right maximizes the right-to-left key,
            # descending left-to-right minimizes it
            fill = "".join(combo) if want_best else "".join(reversed(combo))
            cand = partial + fill
            ck = _key(cand)
            if chosen_key is None or (ck > chosen_key if want_best else ck < chosen_key):
                chosen_key = ck
                chosen = cand
        cache[partial] = chosen
        return chosen

    out = []
    for op in operations:
        kind = op[0]
        if kind == "COMPARE":
            a, b = op[1], op[2]
            ka, kb = _key(a), _key(b)
            if ka > kb:
                out.append("FIRST")
            elif ka < kb:
                out.append("SECOND")
            else:
                out.append("TIE")
        elif kind == "BEST":
            out.append(complete(op[1], True))
        else:
            out.append(complete(op[1], False))
    return out
