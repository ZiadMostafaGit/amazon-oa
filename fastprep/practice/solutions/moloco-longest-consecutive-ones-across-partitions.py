# Ordered reduction of per-partition summaries (prefix/suffix/best/all-ones run of ones).
from typing import List, Optional, Any


def longestDistributedOnes(partitions: List[str]) -> int:
    # summary: (length, prefix ones, suffix ones, best inside)
    total_len = 0
    pre = 0
    suf = 0
    best = 0
    for part in partitions:
        n = len(part)
        p = 0
        while p < n and part[p] == '1':
            p += 1
        s = 0
        while s < n and part[n - 1 - s] == '1':
            s += 1
        b = 0
        run = 0
        for ch in part:
            if ch == '1':
                run += 1
                if run > b:
                    b = run
            else:
                run = 0
        # combine (total_len, pre, suf, best) with (n, p, s, b)
        nbest = max(best, b, suf + p)
        npre = pre if pre < total_len else total_len + p
        nsuf = s if s < n else suf + n
        total_len += n
        pre, suf, best = npre, nsuf, max(nbest, npre, nsuf)
    return best
