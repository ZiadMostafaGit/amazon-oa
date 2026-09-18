# Parse each artifact rectangle into its cell set and count how many searched cells it contains.
from typing import List, Tuple


def _parse_cell(token: str) -> Tuple[int, int]:
    token = token.strip()
    i = 0
    while i < len(token) and token[i].isdigit():
        i += 1
    row = int(token[:i])
    col = ord(token[i:].upper()) - ord('A') + 1
    return row, col


def findHiddenArtifacts(n: int, artifacts: str, searched: str) -> List[int]:
    found = set()
    for tok in searched.split():
        if tok.strip():
            found.add(_parse_cell(tok))

    full = 0
    partial = 0
    for desc in artifacts.split(','):
        desc = desc.strip()
        if not desc:
            continue
        parts = desc.split()
        r1, c1 = _parse_cell(parts[0])
        r2, c2 = _parse_cell(parts[1])
        lo_r, hi_r = min(r1, r2), max(r1, r2)
        lo_c, hi_c = min(c1, c2), max(c1, c2)
        total = 0
        hit = 0
        for r in range(lo_r, hi_r + 1):
            for c in range(lo_c, hi_c + 1):
                total += 1
                if (r, c) in found:
                    hit += 1
        if hit == total and total > 0:
            full += 1
        elif hit > 0:
            partial += 1
    return [full, partial]
