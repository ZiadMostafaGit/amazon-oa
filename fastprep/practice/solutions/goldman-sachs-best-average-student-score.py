# Hash-map aggregation of sum/count per student, exact average comparison via cross-multiplication.
from typing import List, Optional, Any


def bestAverageStudent(records: List[List[str]]) -> str:
    totals = {}
    counts = {}
    for row in records:
        name = row[0]
        score = int(row[1])
        totals[name] = totals.get(name, 0) + score
        counts[name] = counts.get(name, 0) + 1

    best_name = None
    best_sum = 0
    best_cnt = 1
    for name in totals:
        s = totals[name]
        c = counts[name]
        if best_name is None:
            best_name, best_sum, best_cnt = name, s, c
            continue
        # compare s/c vs best_sum/best_cnt  (c, best_cnt > 0)
        left = s * best_cnt
        right = best_sum * c
        if left > right or (left == right and name < best_name):
            best_name, best_sum, best_cnt = name, s, c
    return best_name
