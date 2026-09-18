# Prefix XOR bitmask of letter parities; longest span between two equal masks.
def solution(S: str) -> int:
    first = {0: -1}
    mask = 0
    best = 0
    for i, ch in enumerate(S):
        mask ^= 1 << (ord(ch) - 97)
        if mask in first:
            span = i - first[mask]
            if span > best:
                best = span
        else:
            first[mask] = i
    return best
