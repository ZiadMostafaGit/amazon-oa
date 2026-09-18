# Greedy over runs: every run of length >= 2 is an "engine" that repaints the whole suffix, applied right to left.
from bisect import bisect_left, bisect_right


def getMaximumOperations(s: str) -> int:
    n = len(s)
    if n < 3:
        return 0

    # positions of each character, for O(log n) range counts
    pos = {}
    for i, ch in enumerate(s):
        pos.setdefault(ch, []).append(i)

    def count_char(ch, lo, hi):
        # number of j in [lo, hi] with s[j] == ch
        lst = pos.get(ch)
        if not lst or lo > hi:
            return 0
        return bisect_right(lst, hi) - bisect_left(lst, lo)

    # maximal runs: (char, end index, length)
    engines = []
    i = 0
    while i < n:
        j = i
        while j + 1 < n and s[j + 1] == s[i]:
            j += 1
        if j - i + 1 >= 2:
            engines.append((s[i], j))
        i = j + 1

    total = 0
    e_last = n - 1          # end of the untouched original region
    c_last = None           # char now filling positions (e_last, n-1]
    l_last = 0              # length of that painted region
    for ch, e in reversed(engines):
        if e < n - 1:
            span = e_last - e
            total += span - count_char(ch, e + 1, e_last)
            if c_last is not None and c_last != ch:
                total += l_last
        e_last = e
        c_last = ch
        l_last = n - 1 - e
    return total
