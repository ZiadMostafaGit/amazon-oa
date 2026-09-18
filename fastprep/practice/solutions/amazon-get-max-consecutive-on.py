# Sliding window: longest substring containing at most max_flips maximal runs of zeros.
def getMaxConsecutiveON(machine_status: str, max_flips: int) -> int:
    s = machine_status
    n = len(s)
    # start[i] = 1 when a zero-run begins at i
    pref = [0] * (n + 1)
    for i in range(n):
        pref[i + 1] = pref[i] + (1 if (s[i] == '0' and (i == 0 or s[i - 1] == '1')) else 0)

    def groups(l: int, r: int) -> int:
        # number of zero runs inside window [l, r]
        g = pref[r + 1] - pref[l + 1]
        if s[l] == '0':
            g += 1
        return g

    best = 0
    l = 0
    for r in range(n):
        while l <= r and groups(l, r) > max_flips:
            l += 1
        if r - l + 1 > best:
            best = r - l + 1
    return best
