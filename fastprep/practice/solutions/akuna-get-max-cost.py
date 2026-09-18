# Total travel distance is fixed, so maximize the operation count: gap j (zeros right of the j-th one,
# before the (j+1)-th) contributes j*g_j distance plus j extra operations when it is non-empty.

def getMaxCost(s: str) -> int:
    total = 0
    idx = 0          # index of the current one (1-based), 0 before the first one
    gap = 0          # zeros seen since that one
    for ch in s:
        if ch == '1':
            if idx > 0 and gap > 0:
                total += idx * (gap + 1)
            idx += 1
            gap = 0
        else:
            gap += 1
    if idx > 0 and gap > 0:
        total += idx * (gap + 1)
    return total
