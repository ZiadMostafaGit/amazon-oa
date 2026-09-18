# Hash-map lookup: build due/completion dicts, then classify each query by the rule precedence.
from typing import List, Optional, Any


def trainingStatuses(queryEmployeeIds: List[str], requiredEmployeeIds: List[str], dueDays: List[int], completedEmployeeIds: List[str], completionDays: List[int], checkDay: int) -> List[str]:
    due = {}
    for i, emp in enumerate(requiredEmployeeIds):
        due[emp] = dueDays[i]
    done = {}
    for i, emp in enumerate(completedEmployeeIds):
        done[emp] = completionDays[i]

    out = []
    for emp in queryEmployeeIds:
        if emp not in due:
            out.append("NOT_REQUIRED")
        elif emp in done and done[emp] <= checkDay:
            out.append("COMPLETED")
        elif checkDay > due[emp]:
            out.append("OVERDUE")
        else:
            out.append("PENDING")
    return out
