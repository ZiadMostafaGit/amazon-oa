# Hash-map tally of report events, replayed over the operation list.
from typing import List, Optional, Any


def countSpamReports(operations: List[str]) -> List[int]:
    counts = {}
    results: List[int] = []
    for op in operations:
        command, _, number = op.partition(" ")
        number = number.strip()
        if command == "REPORT":
            counts[number] = counts.get(number, 0) + 1
        elif command == "COUNT":
            results.append(counts.get(number, 0))
    return results
