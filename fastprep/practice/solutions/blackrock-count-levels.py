from typing import List


def countLevels(employeePairs: List[List[str]], employee1: str, employee2: str) -> int:
    manager = {}
    for emp, mgr in employeePairs:
        manager[emp] = mgr
    depth_cache = {}

    def depth(name):
        # Levels from name up to the top of the hierarchy (top person = 0).
        path = []
        while name not in depth_cache and name in manager:
            path.append(name)
            name = manager[name]
        d = depth_cache.get(name, 0)
        depth_cache[name] = d
        for p in reversed(path):
            d += 1
            depth_cache[p] = d
        return d

    return abs(depth(employee1) - depth(employee2))
