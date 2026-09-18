# Event simulation: account incarnations with balance history plus a min-heap of due scheduled payments.
import heapq
from bisect import bisect_right
from typing import List, Optional, Any


class _Account:
    __slots__ = ("aid", "balance", "outgoing", "created", "closed", "times", "bals")

    def __init__(self, aid, created):
        self.aid = aid
        self.balance = 0
        self.outgoing = 0
        self.created = created
        self.closed = None
        self.times = [created]
        self.bals = [0]

    def record(self, t):
        if self.times and self.times[-1] == t:
            self.bals[-1] = self.balance
        else:
            self.times.append(t)
            self.bals.append(self.balance)

    def at(self, t):
        i = bisect_right(self.times, t)
        if i == 0:
            return None
        return self.bals[i - 1]


class _Payment:
    __slots__ = ("pid", "due", "seq", "acct", "amount")

    def __init__(self, pid, due, seq, acct, amount):
        self.pid = pid
        self.due = due
        self.seq = seq
        self.acct = acct
        self.amount = amount


def processBankingQueries(queries: List[List[str]]) -> List[str]:
    history = {}          # account id -> list of incarnations, oldest first
    active = {}           # account id -> current open incarnation
    pending = {}          # payment id -> _Payment
    heap = []             # (due, seq, pid)
    payment_counter = 0
    seq_counter = 0
    out = []

    def run_due(t):
        while heap and heap[0][0] <= t:
            due, _seq, pid = heapq.heappop(heap)
            p = pending.pop(pid, None)
            if p is None:
                continue
            acct = p.acct
            if acct.closed is None and acct.balance >= p.amount:
                acct.balance -= p.amount
                acct.outgoing += p.amount
                acct.record(due)

    for q in queries:
        op = q[0]
        t = int(q[1])
        run_due(t)

        if op == "CREATE_ACCOUNT":
            aid = q[2]
            if aid in active:
                out.append("false")
            else:
                acc = _Account(aid, t)
                active[aid] = acc
                history.setdefault(aid, []).append(acc)
                out.append("true")

        elif op == "DEPOSIT":
            aid = q[2]
            amount = int(q[3])
            acc = active.get(aid)
            if acc is None:
                out.append("")
            else:
                acc.balance += amount
                acc.record(t)
                out.append(str(acc.balance))

        elif op == "TRANSFER":
            src_id, dst_id = q[2], q[3]
            amount = int(q[4])
            src = active.get(src_id)
            dst = active.get(dst_id)
            if src is None or dst is None or src_id == dst_id or src.balance < amount:
                out.append("")
            else:
                src.balance -= amount
                src.outgoing += amount
                dst.balance += amount
                src.record(t)
                dst.record(t)
                out.append(str(src.balance))

        elif op == "TOP_SPENDERS":
            n = int(q[2])
            ranked = sorted(active.values(), key=lambda a: (-a.outgoing, a.aid))[:n]
            out.append(",".join("%s(%d)" % (a.aid, a.outgoing) for a in ranked))

        elif op == "SCHEDULE_PAYMENT":
            aid = q[2]
            amount = int(q[3])
            delay = int(q[4])
            acc = active.get(aid)
            if acc is None:
                out.append("")
            else:
                payment_counter += 1
                pid = "payment%d" % payment_counter
                seq_counter += 1
                p = _Payment(pid, t + delay, seq_counter, acc, amount)
                pending[pid] = p
                heapq.heappush(heap, (p.due, p.seq, pid))
                out.append(pid)

        elif op == "CANCEL_PAYMENT":
            aid = q[2]
            pid = q[3]
            acc = active.get(aid)
            p = pending.get(pid)
            if acc is None or p is None or p.acct is not acc:
                out.append("false")
            else:
                del pending[pid]
                out.append("true")

        elif op == "MERGE_ACCOUNTS":
            sid, aid = q[2], q[3]
            surv = active.get(sid)
            absorbed = active.get(aid)
            if surv is None or absorbed is None or sid == aid:
                out.append("false")
            else:
                surv.balance += absorbed.balance
                surv.outgoing += absorbed.outgoing
                for p in pending.values():
                    if p.acct is absorbed:
                        p.acct = surv
                absorbed.balance = 0
                absorbed.closed = t
                surv.record(t)
                del active[aid]
                out.append("true")

        elif op == "GET_BALANCE":
            aid = q[2]
            time_at = int(q[3])
            ans = ""
            for acc in history.get(aid, ()):
                if acc.created <= time_at and (acc.closed is None or time_at < acc.closed):
                    v = acc.at(time_at)
                    if v is not None:
                        ans = str(v)
                    break
            out.append(ans)

    return out
