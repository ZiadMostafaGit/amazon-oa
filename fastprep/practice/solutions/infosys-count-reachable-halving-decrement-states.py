# BFS level by level over reachable values, at most `steps` levels; visited set counts distinct states.
def countReachableValues(num: int, steps: int) -> int:
    visited = {num}
    frontier = [num]
    for _ in range(steps):
        if not frontier:
            break
        nxt = []
        for v in frontier:
            if v % 2 == 0:
                h = v // 2
                if h not in visited:
                    visited.add(h)
                    nxt.append(h)
            if v > 0:
                d = v - 1
                if d not in visited:
                    visited.add(d)
                    nxt.append(d)
        frontier = nxt
    return len(visited)
