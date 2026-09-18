# Kahn topological sort over the reference graph; leftover nodes mean a cycle.
from typing import List
from collections import deque


def evaluateFormulas(formulas: List[str]) -> List[str]:
    names = []
    base = {}
    deps = {}       # name -> list of (sign, dep_name)
    dependents = {} # dep_name -> list of names depending on it
    indeg = {}

    for line in formulas:
        tok = line.split()
        name = tok[0]
        names.append(name)
        b = 0
        dl = []
        sign = 1
        i = 2
        while i < len(tok):
            t = tok[i]
            if t == '+':
                sign = 1
            elif t == '-':
                sign = -1
            else:
                neg = t[0] == '-'
                body = t[1:] if (neg or t[0] == '+') else t
                if body.isdigit():
                    b += sign * int(t)
                else:
                    dl.append((sign, t))
                sign = 1
            i += 1
        base[name] = b
        deps[name] = dl
        indeg[name] = len(dl)
        dependents.setdefault(name, [])

    for name, dl in deps.items():
        for _, d in dl:
            dependents.setdefault(d, []).append(name)

    value = {}
    q = deque(n for n in names if indeg[n] == 0)
    done = 0
    while q:
        n = q.popleft()
        v = base[n]
        for sign, d in deps[n]:
            v += sign * value[d]
        value[n] = v
        done += 1
        for p in dependents.get(n, ()):
            indeg[p] -= 1
            if indeg[p] == 0:
                q.append(p)

    if done != len(names):
        return ["CYCLE"]
    return [n + "=" + str(value[n]) for n in names]
