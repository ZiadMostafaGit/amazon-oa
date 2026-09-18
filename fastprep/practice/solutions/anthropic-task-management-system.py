# Direct simulation: hash maps for users/tasks plus a lazy min-heap keyed on expiry time.
from typing import List, Optional, Any
import heapq

ACTIVE = "ACTIVE"
COMPLETED = "COMPLETED"
EXPIRED = "EXPIRED"
DELETED = "DELETED"


def processTaskOperations(operations: List[List[str]]) -> List[List[str]]:
    users = {}          # userId -> [quota, activeCount, [taskId, ...] in creation order]
    tasks = {}          # taskId -> [userId, priority, createdAt, dueAt, expiresAt, status]
    pending = []        # lazy heap of (expiresAt, taskId)
    out = []

    def expire(now):
        while pending and pending[0][0] <= now:
            exp, tid = heapq.heappop(pending)
            rec = tasks[tid]
            if rec[5] == ACTIVE and rec[4] == exp:
                rec[5] = EXPIRED
                users[rec[0]][1] -= 1

    for op in operations:
        kind = op[0]
        now = int(op[1])
        expire(now)

        if kind == "ADD_USER":
            users[op[2]] = [int(op[3]), 0, []]
            out.append(["OK"])

        elif kind == "CREATE":
            tid, uid = op[2], op[3]
            if tid in tasks:
                out.append(["DUPLICATE_TASK"])
            elif uid not in users:
                out.append(["UNKNOWN_USER"])
            else:
                user = users[uid]
                if user[1] >= user[0]:
                    out.append(["QUOTA_EXCEEDED"])
                else:
                    exp = int(op[6])
                    tasks[tid] = [uid, int(op[4]), now, int(op[5]), exp, ACTIVE]
                    user[1] += 1
                    user[2].append(tid)
                    heapq.heappush(pending, (exp, tid))
                    out.append(["OK"])

        elif kind == "GET":
            rec = tasks.get(op[2])
            if rec is None or rec[5] == DELETED:
                out.append([])
            else:
                out.append([op[2], rec[0], str(rec[1]), str(rec[2]), str(rec[3]), str(rec[4]), rec[5]])

        elif kind == "UPDATE":
            rec = tasks.get(op[2])
            if rec is None or rec[5] == DELETED:
                out.append(["NOT_FOUND"])
            elif rec[5] != ACTIVE:
                out.append(["NOT_ACTIVE"])
            else:
                rec[1] = int(op[3])
                rec[3] = int(op[4])
                rec[4] = int(op[5])
                heapq.heappush(pending, (rec[4], op[2]))
                out.append(["OK"])

        elif kind == "DELETE":
            rec = tasks.get(op[2])
            if rec is None or rec[5] == DELETED:
                out.append(["NOT_FOUND"])
            else:
                if rec[5] == ACTIVE:
                    users[rec[0]][1] -= 1
                rec[5] = DELETED
                out.append(["OK"])

        elif kind == "COMPLETE":
            rec = tasks.get(op[2])
            if rec is None or rec[5] == DELETED:
                out.append(["NOT_FOUND"])
            elif rec[5] != ACTIVE:
                out.append(["NOT_ACTIVE"])
            else:
                rec[5] = COMPLETED
                users[rec[0]][1] -= 1
                out.append(["OK"])

        elif kind == "SET_QUOTA":
            user = users.get(op[2])
            if user is None:
                out.append(["UNKNOWN_USER"])
            else:
                user[0] = int(op[3])
                out.append(["OK"])

        elif kind == "SEARCH":
            user = users.get(op[2])
            if user is None:
                out.append(["UNKNOWN_USER"])
            else:
                rows = [(-tasks[t][1], tasks[t][2], t) for t in user[2] if tasks[t][5] == ACTIVE]
                rows.sort()
                out.append([r[2] for r in rows])

        elif kind == "HISTORY":
            user = users.get(op[2])
            if user is None:
                out.append(["UNKNOWN_USER"])
            else:
                view = op[3]
                found = []
                for t in user[2]:
                    rec = tasks[t]
                    st = rec[5]
                    if view == "COMPLETED":
                        keep = st == COMPLETED
                    elif view == "EXPIRED":
                        keep = st == EXPIRED
                    elif view == "UNFINISHED":
                        keep = st == ACTIVE
                    else:  # OVERDUE
                        keep = st == ACTIVE and rec[3] < now
                    if keep:
                        found.append((rec[2], t))
                found.sort()
                out.append([t for _, t in found])

        else:
            out.append([])

    return out
