def countThreeSisters(l: int, r: int) -> int:
    count = 0
    for x in range(l, r + 1):
        s = str(x)
        if len(set(s)) == len(s):
            count += 1
    return count
