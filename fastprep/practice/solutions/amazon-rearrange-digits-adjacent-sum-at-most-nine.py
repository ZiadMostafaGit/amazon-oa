# Greedy largest-first placement, validated at each step by a Hall-condition feasibility test
# on the remaining multiset (highs >=5 must sit in non-adjacent gaps between the sorted lows).


def _feasible(cnt, B):
    """Can the remaining multiset `cnt` be arranged so that every adjacent sum <= 9
    and the first digit is <= B?"""
    L = cnt[0] + cnt[1] + cnt[2] + cnt[3] + cnt[4]
    H = cnt[5] + cnt[6] + cnt[7] + cnt[8] + cnt[9]
    if L == 0 and H == 0:
        return True
    if B <= 4:
        # nothing >= 5 may come first, so the first digit must be a low digit <= B
        if L == 0:
            return False
        if not any(cnt[d] for d in range(0, B + 1)):
            return False
    # prefix counts of low digits
    pre = [0] * 5
    run = 0
    for d in range(5):
        run += cnt[d]
        pre[d] = run
    # suffix counts of high digits
    suf = [0] * 11
    for v in range(9, 4, -1):
        suf[v] = suf[v + 1] + cnt[v]
    for v in range(5, 10):
        hv = suf[v]
        if hv == 0:
            continue
        t = 9 - v                      # a gap holding value v needs all neighbours <= t
        m = pre[t]                     # lows that are <= t
        if L == 0:
            g = 1 if v <= B else 0
        else:
            base = L if m == L else (m - 1 if m >= 1 else 0)
            g = base + (1 if (m >= 1 and v <= B) else 0)
        if hv > g:
            return False
    return True


def rearrangeDigits(digits: str) -> str:
    cnt = [0] * 10
    for ch in digits:
        cnt[ord(ch) - 48] += 1
    if not _feasible(cnt, 9):
        return ""
    out = []
    n = len(digits)
    B = 9
    remaining_high = sum(cnt[5:])
    while len(out) < n:
        if remaining_high == 0:
            # only low digits left: any order works, so take the largest allowed first
            first = -1
            for d in range(min(B, 4), -1, -1):
                if cnt[d]:
                    first = d
                    break
            out.append(first)
            cnt[first] -= 1
            for d in range(4, -1, -1):
                out.extend([d] * cnt[d])
                cnt[d] = 0
            break
        for d in range(min(B, 9), -1, -1):
            if not cnt[d]:
                continue
            cnt[d] -= 1
            if _feasible(cnt, 9 - d):
                out.append(d)
                if d >= 5:
                    remaining_high -= 1
                B = 9 - d
                break
            cnt[d] += 1
        else:
            return ""
    return "".join(chr(48 + d) for d in out)
