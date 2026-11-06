from typing import List


def findSchedules(work_hours: int, day_hours: int, pattern: str) -> List[str]:
    slots = [i for i, c in enumerate(pattern) if c == '?']
    remaining = work_hours - sum(int(c) for c in pattern if c != '?')
    cur = list(pattern)
    out = []

    def go(k, left):
        if k == len(slots):
            if left == 0:
                out.append(''.join(cur))
            return
        rest = len(slots) - k - 1
        for h in range(0, min(day_hours, left) + 1):
            if left - h > rest * day_hours:
                continue
            cur[slots[k]] = str(h)
            go(k + 1, left - h)
        cur[slots[k]] = '?'

    if remaining >= 0:
        go(0, remaining)
    return out
