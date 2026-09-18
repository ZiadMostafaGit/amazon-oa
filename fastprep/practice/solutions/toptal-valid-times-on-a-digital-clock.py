# Brute force over all permutations of the four digits, collecting distinct valid HH:MM strings.
from itertools import permutations


def solution(a: int, b: int, c: int, d: int) -> int:
    seen = set()
    for p in permutations([a, b, c, d]):
        hh = p[0] * 10 + p[1]
        mm = p[2] * 10 + p[3]
        if 0 <= hh <= 23 and 0 <= mm <= 59:
            seen.add((hh, mm))
    return len(seen)
