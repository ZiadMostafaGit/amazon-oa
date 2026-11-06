from typing import List


def optimalUtilization(deviceCapacity: int, foregroundAppList: List[List[int]], backgroundAppList: List[List[int]]) -> List[List[int]]:
    fg = sorted(foregroundAppList, key=lambda a: a[1])
    bg = sorted(backgroundAppList, key=lambda a: a[1])
    best = -1
    pairs: List[List[int]] = []
    i, j = 0, len(bg) - 1
    while i < len(fg) and j >= 0:
        s = fg[i][1] + bg[j][1]
        if s > deviceCapacity:
            j -= 1
            continue
        if s > best:
            best, pairs = s, []
        if s == best:
            # every background app with this same memory pairs with fg[i]
            k = j
            while k >= 0 and bg[k][1] == bg[j][1]:
                pairs.append([fg[i][0], bg[k][0]])
                k -= 1
        i += 1
    if not pairs:
        return [[]]
    pairs.sort()
    return pairs
