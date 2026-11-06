from typing import List


def processData(n: int, arr: List[int]) -> List[int]:
    a = sorted(arr)

    def special(x):
        last, rem = x % 10, x // 10
        return rem + rem * last + last == x

    out = []
    stack = [(0, len(a) - 1)]  # segments still to emit, preorder via stack
    while stack:
        lo, hi = stack.pop()
        if lo > hi:
            continue
        mid = lo + (hi - lo) // 2
        x = a[mid]
        out.append(0 if special(x) else x)
        stack.append((mid + 1, hi))  # right pushed first so left is emitted first
        stack.append((lo, mid - 1))
    return out
