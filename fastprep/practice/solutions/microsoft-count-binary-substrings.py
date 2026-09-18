# Compare adjacent run lengths: each neighboring pair contributes min(prev_run, cur_run).
def countBinarySubstrings(s: str) -> int:
    total = 0
    prev = 0
    cur = 0
    last = ''
    for ch in s:
        if ch == last:
            cur += 1
        else:
            total += min(prev, cur)
            prev = cur
            cur = 1
            last = ch
    return total + min(prev, cur)
