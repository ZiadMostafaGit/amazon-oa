# Simulation: per-server consecutive-failure counters with permanently opening breakers.
from typing import List, Optional, Any


def routeDatabaseRequests(outcomes: List[List[str]]) -> List[str]:
    names = ["PRIMARY", "REPLICA_1", "REPLICA_2"]
    fails = [0, 0, 0]
    is_open = [False, False, False]
    results = []
    for row in outcomes:
        picked = "FAILED"
        for i in range(3):
            if is_open[i]:
                continue
            if row[i] == "SUCCESS":
                fails[i] = 0
                picked = names[i]
                break
            fails[i] += 1
            if fails[i] >= 2:
                is_open[i] = True
        results.append(picked)
    return results
