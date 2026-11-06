def closestLandMark(aNum: int) -> int:
    a, b = 0, 1
    best = abs(aNum - a)
    while a <= aNum:
        a, b = b, a + b
        best = min(best, abs(aNum - a))
    return best
