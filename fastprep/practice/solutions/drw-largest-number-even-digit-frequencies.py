# Greedy: keep max length (drop one 1 and/or one 2 for parity), deleting each at the position that leaves the largest string.
def solution(digits: str) -> str:
    c1 = digits.count('1')
    c2 = len(digits) - c1
    need = []
    if c1 % 2:
        need.append('1')
    if c2 % 2:
        need.append('2')
    if not need:
        return digits
    if len(need) == 1:
        return _delete_one(digits, need[0])
    a = _delete_one(_delete_one(digits, '1'), '2')
    b = _delete_one(_delete_one(digits, '2'), '1')
    return a if a >= b else b


def _delete_one(s: str, d: str) -> str:
    # remove one occurrence of digit d so the remaining string is lexicographically largest
    last = -1
    for i, ch in enumerate(s):
        if ch == d:
            last = i
            if i + 1 < len(s) and s[i + 1] > ch:
                return s[:i] + s[i + 1:]
    if last < 0:
        return s
    return s[:last] + s[last + 1:]
