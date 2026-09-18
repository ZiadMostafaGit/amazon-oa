# Approach: direct simulation of Fibonacci-capacity levels with reachability, weight/id selection and falling nuts.
from typing import List, Optional, Any


def _num(s: str) -> int:
    # decimal with up to 3 fraction digits -> integer thousandths
    s = s.strip()
    neg = s.startswith("-")
    if neg:
        s = s[1:]
    if "." in s:
        whole, frac = s.split(".", 1)
    else:
        whole, frac = s, ""
    frac = (frac + "000")[:3]
    v = int(whole or "0") * 1000 + int(frac or "0")
    return -v if neg else v


def _caps(n: int) -> List[int]:
    caps = []
    a, b = 1, 2
    for _ in range(n):
        caps.append(a)
        a, b = b, a + b
    return caps


def simulateSquirrelResearch(locations: List[str], operations: List[str]) -> List[str]:
    caps = {}
    levels = {}
    for entry in locations:
        lid, _, lv = entry.rpartition(":")
        n = int(lv.strip())
        lid = lid.strip()
        caps[lid] = _caps(n)
        levels[lid] = [[] for _ in range(n)]

    active = {}  # nut_id -> location id
    out = []

    for op in operations:
        parts = op.split()
        kind = parts[0]
        if kind == "HideNut":
            _, ts, lid, nid, w, ttl = parts[0], parts[1], parts[2], parts[3], parts[4], parts[5]
            if lid not in caps or nid in active:
                out.append("false")
                continue
            lv = levels[lid]
            cp = caps[lid]
            placed = False
            for i in range(len(lv)):
                if len(lv[i]) < cp[i]:
                    lv[i].append((_num(w), nid, _num(ts), _num(ttl)))
                    active[nid] = lid
                    placed = True
                    break
            out.append("true" if placed else "false")
        else:
            ts = _num(parts[1])
            lid = parts[2]
            cap_nuts = int(parts[3])
            if lid not in caps:
                out.append("[]")
                continue
            lv = levels[lid]
            cp = caps[lid]
            got = []
            examined = 0
            while examined < cap_nuts:
                top = -1
                for i in range(len(lv) - 1, -1, -1):
                    if lv[i]:
                        top = i
                        break
                if top < 0:
                    break
                reach = [top]
                if len(lv[top]) * 2 < cp[top] and top - 1 >= 0:
                    reach.append(top - 1)
                best = None
                best_lvl = -1
                for li in reach:
                    for nut in lv[li]:
                        if best is None or nut[0] > best[0] or (nut[0] == best[0] and nut[1] < best[1]):
                            best = nut
                            best_lvl = li
                lv[best_lvl].remove(best)
                del active[best[1]]
                examined += 1
                if ts <= best[2] + best[3]:
                    got.append(best[1])
                if best_lvl == top - 1 and lv[top]:
                    faller = None
                    for nut in lv[top]:
                        if faller is None or nut[0] < faller[0] or (nut[0] == faller[0] and nut[1] < faller[1]):
                            faller = nut
                    lv[top].remove(faller)
                    lv[best_lvl].append(faller)
            out.append("[" + ",".join(got) + "]")
    return out
