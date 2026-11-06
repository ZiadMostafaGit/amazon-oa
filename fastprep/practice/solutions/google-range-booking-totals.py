from typing import List


def solve(bookings: List[List[int]], n: int) -> List[int]:
    diff = [0] * (n + 2)
    for start, end, units in bookings:
        diff[start] += units
        diff[end + 1] -= units
    out = []
    run = 0
    for slot in range(1, n + 1):
        run += diff[slot]
        out.append(run)
    return out
