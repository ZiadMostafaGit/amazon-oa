# Direct simulation with a task dictionary and per-query sorting by the stated key orders.
from typing import List, Optional, Any


def processTaskOperations(operations: List[List[str]]) -> List[List[str]]:
    tasks = {}  # taskId -> dict
    out = []

    for op in operations:
        kind = op[0]
        ts = int(op[1])

        if kind == "WRITE":
            task_id, text, priority, due_at = op[2], op[3], op[4], op[5]
            existing = tasks.get(task_id)
            if existing is None:
                tasks[task_id] = {
                    "id": task_id,
                    "text": text,
                    "priority": priority,
                    "due": due_at,
                    "assignee": "",
                    "status": "OPEN",
                }
                out.append(["OK"])
            elif existing["status"] == "COMPLETED":
                out.append(["NOT_ACTIVE"])
            else:
                existing["text"] = text
                existing["priority"] = priority
                existing["due"] = due_at
                out.append(["OK"])

        elif kind == "READ":
            task = tasks.get(op[2])
            if task is None:
                out.append([])
            else:
                out.append([task["id"], task["text"], task["priority"],
                            task["due"], task["assignee"], task["status"]])

        elif kind == "SEARCH":
            query = op[2]
            matches = [t for t in tasks.values()
                       if t["status"] != "COMPLETED" and query in t["text"]]
            matches.sort(key=lambda t: (-int(t["priority"]), t["id"]))
            out.append([t["id"] for t in matches])

        elif kind == "LIST":
            active = [t for t in tasks.values() if t["status"] != "COMPLETED"]
            active.sort(key=lambda t: (-int(t["priority"]), t["id"]))
            out.append([t["id"] for t in active])

        elif kind == "ASSIGN":
            task = tasks.get(op[2])
            if task is None:
                out.append(["NOT_FOUND"])
            elif task["status"] == "COMPLETED":
                out.append(["NOT_ACTIVE"])
            else:
                task["assignee"] = op[3]
                task["status"] = "ASSIGNED"
                out.append(["OK"])

        elif kind == "COMPLETE":
            task = tasks.get(op[2])
            if task is None:
                out.append(["NOT_FOUND"])
            elif task["status"] == "COMPLETED":
                out.append(["NOT_ACTIVE"])
            elif task["status"] == "OPEN":
                out.append(["NOT_ASSIGNED"])
            else:
                task["status"] = "COMPLETED"
                out.append(["OK"])

        elif kind == "CHECK_OVERDUE":
            user = op[2]
            overdue = [t for t in tasks.values()
                       if t["status"] != "COMPLETED" and t["assignee"] == user
                       and int(t["due"]) < ts]
            overdue.sort(key=lambda t: (int(t["due"]), t["id"]))
            out.append([t["id"] for t in overdue])

        else:
            out.append([])

    return out
