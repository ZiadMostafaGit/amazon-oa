# Brute force over all 100 digit-replacement pairs, rejecting leading zeros.
def findRange(num: int) -> int:
    s = str(num)
    best = None
    worst = None
    for src in "0123456789":
        for dst in "0123456789":
            candidate = s.replace(src, dst)
            if candidate[0] == '0':
                continue
            value = int(candidate)
            if best is None or value > best:
                best = value
            if worst is None or value < worst:
                worst = value
    return best - worst
