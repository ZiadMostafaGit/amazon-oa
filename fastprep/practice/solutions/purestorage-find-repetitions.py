# Scan every occurrence position of short_s, then extend greedily by block strides.
def findRepetitions(short_s: str, long_s: str) -> int:
    if not short_s or not long_s:
        return 0
    m = len(short_s)
    n = len(long_s)
    if m > n:
        return 0
    # Mark all starting positions where short_s occurs.
    occ = bytearray(n)
    pos = long_s.find(short_s)
    while pos != -1:
        occ[pos] = 1
        pos = long_s.find(short_s, pos + 1)
    best = 0
    # run[i] = longest chain of adjacent blocks starting at i, computed right to left.
    run = [0] * (n + 1)
    for i in range(n - 1, -1, -1):
        if occ[i]:
            nxt = i + m
            run[i] = 1 + (run[nxt] if nxt < n else 0)
            if run[i] > best:
                best = run[i]
    return best
