from typing import List


def analyzeTree(values: List[int], children: List[List[int]]) -> List[str]:
    n = len(values)
    total = sum(values)
    order = [0]
    for v in order:
        for c in children[v]:
            if c != -1:
                order.append(c)
    down = [0] * n       # best downward path sum starting at v
    nxt = [-1] * n       # next node on that best downward path (-1 = stop)
    best = None
    best_node = -1
    for v in reversed(order):
        l, r = children[v]
        gl = down[l] if l != -1 and down[l] > 0 else 0
        gr = down[r] if r != -1 and down[r] > 0 else 0
        if gl >= gr and gl > 0:
            down[v], nxt[v] = values[v] + gl, l
        elif gr > 0:
            down[v], nxt[v] = values[v] + gr, r
        else:
            down[v], nxt[v] = values[v], -1
        through = values[v] + gl + gr
        if best is None or through > best:
            best, best_node = through, v

    def chain(u):
        res = []
        while u != -1:
            res.append(values[u])
            u = nxt[u]
        return res

    v = best_node
    l, r = children[v]
    left = chain(l) if l != -1 and down[l] > 0 else []
    right = chain(r) if r != -1 and down[r] > 0 else []
    path = left[::-1] + [values[v]] + right
    return [str(total), str(best), " ".join(map(str, path))]
