# Dependency DAG with unsatisfied-dependency counters plus a BFS failure cascade over blocked dependents.
from typing import List, Optional, Any
from collections import deque

_ORDER = {
    "BLOCKED": 0,
    "READY_TO_EXECUTE": 1,
    "IN_PROGRESS": 2,
    "SUCCEEDED": 3,
    "FAILED": 4,
}
_TERMINAL = {"SUCCEEDED", "FAILED"}


def runAgentTodoList(operations: List[List[str]]) -> List[str]:
    desc: List[str] = []
    status: List[str] = []
    deps: List[List[int]] = []
    dependents: List[List[int]] = []
    pending: List[int] = []  # count of dependencies not yet SUCCEEDED
    out: List[str] = []

    for op in operations:
        kind = op[0]
        if kind == "ADD":
            tid = len(desc) + 1
            d = sorted(int(x) for x in op[2:])
            desc.append(op[1])
            deps.append(d)
            dependents.append([])
            waiting = 0
            for dep in d:
                dependents[dep - 1].append(tid)
                if status[dep - 1] != "SUCCEEDED":
                    waiting += 1
            pending.append(waiting)
            st = "READY_TO_EXECUTE" if waiting == 0 else "BLOCKED"
            status.append(st)
            out.append("%d:%s" % (tid, st))
        elif kind == "GET":
            tid = int(op[1])
            if 1 <= tid <= len(desc):
                out.append("%d|%s|%s" % (tid, status[tid - 1], desc[tid - 1]))
            else:
                out.append("NULL")
        elif kind == "SET":
            tid = int(op[1])
            new = op[2]
            if not (1 <= tid <= len(desc)):
                out.append("false")
                continue
            cur = status[tid - 1]
            if cur in _TERMINAL or _ORDER[new] <= _ORDER[cur]:
                out.append("false")
                continue
            status[tid - 1] = new
            if new == "SUCCEEDED":
                for child in dependents[tid - 1]:
                    pending[child - 1] -= 1
                    if pending[child - 1] == 0 and status[child - 1] == "BLOCKED":
                        status[child - 1] = "READY_TO_EXECUTE"
            elif new == "FAILED":
                queue = deque([tid])
                while queue:
                    cur_id = queue.popleft()
                    for child in dependents[cur_id - 1]:
                        if status[child - 1] == "BLOCKED":
                            status[child - 1] = "FAILED"
                            queue.append(child)
            out.append("true")
        elif kind == "RENDER":
            lines = []
            for idx in range(len(desc)):
                d = deps[idx]
                dep_str = ",".join(str(x) for x in d) if d else "-"
                lines.append("%d|%s|%s|%s" % (idx + 1, status[idx], dep_str, desc[idx]))
            out.append("\n".join(lines))
        else:
            out.append("")
    return out
