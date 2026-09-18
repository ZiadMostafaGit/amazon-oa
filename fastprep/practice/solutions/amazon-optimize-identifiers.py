# Single pass: shortest substring starting with s[0] and ending with s[-1].
def optimizeIdentifiers(s: str) -> int:
    n = len(s)
    first, last = s[0], s[-1]
    best = n
    prev = -1
    for j, ch in enumerate(s):
        if ch == first:
            prev = j
        if ch == last and prev != -1:
            length = j - prev + 1
            if length < best:
                best = length
    return n - best
