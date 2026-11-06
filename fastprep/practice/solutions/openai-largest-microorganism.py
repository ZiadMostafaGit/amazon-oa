from typing import List, Optional, Any


def largestMicroorganism(families: List[str], sizes: List[int]) -> str:
    line = [[f, s] for f, s in zip(families, sizes)]
    while True:
        used = [False] * len(line)  # ate (or was eaten) this round
        ate = False
        i = 0
        while i < len(line):
            if used[i]:
                i += 1
                continue
            f, s = line[i]
            if i > 0 and not used[i - 1] and line[i - 1][0] != f and line[i - 1][1] < s:
                line[i][1] += line[i - 1][1]
                del line[i - 1]
                del used[i - 1]
                i -= 1
                used[i] = True
                ate = True
            elif i + 1 < len(line) and not used[i + 1] and line[i + 1][0] != f and line[i + 1][1] < s:
                line[i][1] += line[i + 1][1]
                del line[i + 1]
                del used[i + 1]
                used[i] = True
                ate = True
            i += 1
        if not ate:
            break
    f, s = max(line, key=lambda t: t[1])
    return "%s %d" % (f, s)
