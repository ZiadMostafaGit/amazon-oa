def countValidSubstrings(s: str, target: str) -> int:
    m = len(target)
    pos = {}
    for j, c in enumerate(target):
        pos.setdefault(c, []).append(j)
    for c in pos:
        pos[c].reverse()  # process larger j first so f[j-1] is still the old value
    # f[j]: latest start l such that target[:j+1] is a subsequence of s[l..r]
    f = [-1] * m
    total = 0
    for r, c in enumerate(s):
        js = pos.get(c)
        if js:
            for j in js:
                if j == 0:
                    f[0] = r
                elif f[j - 1] > f[j]:
                    f[j] = f[j - 1]
        last = f[m - 1]
        total += r - last if last >= 0 else r + 1
    return total
