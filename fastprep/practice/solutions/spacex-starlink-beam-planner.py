# Constructive greedy: per user pick the least-loaded visible satellite, then the first
# of the 4 colors whose already-assigned beams are all >= 10 degrees away.
import math
from typing import List

COS45 = math.cos(math.radians(45.0))
COS10 = math.cos(math.radians(10.0))
EPS = 1e-9


def _dot(a, b):
    return a[0] * b[0] + a[1] * b[1] + a[2] * b[2]


def _norm(a):
    return math.sqrt(_dot(a, a))


def planBeams(users: List[List[float]], satellites: List[List[float]], minimumServed: int) -> List[List[int]]:
    nu = len(users)
    ns = len(satellites)

    # unit beam vector sat -> user, and visibility test, precomputed lazily per pair
    load = [0] * ns
    # beams[s][color] = list of unit vectors from satellite s to its served users
    beams = [[[] for _ in range(4)] for _ in range(ns)]

    result = []

    for ui in range(nu):
        u = users[ui]
        un = _norm(u)
        if un == 0.0:
            continue
        # satellites ordered by current load so beams spread out
        order = sorted(range(ns), key=lambda s: (load[s], s))
        placed = False
        for si in order:
            if load[si] >= 32:
                continue
            s = satellites[si]
            d = (s[0] - u[0], s[1] - u[1], s[2] - u[2])
            dn = _norm(d)
            if dn == 0.0:
                continue
            # user visibility: angle(U, S - U) <= 45 degrees
            if _dot(u, d) < COS45 * un * dn - EPS * un * dn:
                continue
            # unit vector from satellite toward the user
            bx, by, bz = -d[0] / dn, -d[1] / dn, -d[2] / dn
            for color in range(4):
                ok = True
                for (ox, oy, oz) in beams[si][color]:
                    c = bx * ox + by * oy + bz * oz
                    # same color requires angle >= 10 degrees, i.e. cos <= cos(10)
                    if c > COS10 + EPS:
                        ok = False
                        break
                if ok:
                    beams[si][color].append((bx, by, bz))
                    load[si] += 1
                    result.append([ui, si, color + 1])
                    placed = True
                    break
            if placed:
                break

    # serving more than minimumServed users is allowed, so keep every beam found
    return result
