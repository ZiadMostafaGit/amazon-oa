# Bucket subtasks by parent id, then emit tasks sorted by (date, id) with their sorted subtasks.
from typing import List, Optional, Any


def buildTaskHierarchy(records: List[List[str]]) -> List[str]:
    tasks = []
    children = {}
    for rec in records:
        kind = rec[1]
        if kind == "task":
            date, _, task_id, name = rec[0], rec[1], rec[2], rec[3]
            tasks.append((date, task_id, name))
        elif kind == "subtask":
            date, _, sub_id, parent_id, name = rec[0], rec[1], rec[2], rec[3], rec[4]
            children.setdefault(parent_id, []).append((date, sub_id, name))

    tasks.sort(key=lambda t: (t[0], t[1]))
    out = []
    for date, task_id, name in tasks:
        out.append("TASK|" + task_id + "|" + name)
        kids = children.get(task_id)
        if kids:
            kids.sort(key=lambda t: (t[0], t[1]))
            for _, sub_id, sub_name in kids:
                out.append("SUBTASK|" + sub_id + "|" + sub_name)
    return out
