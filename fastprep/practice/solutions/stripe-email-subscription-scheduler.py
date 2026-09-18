# Simulation: expand each user's schedule into dated emails, apply plan changes and renewals, then sort by day.
from typing import List, Optional, Any


def sendSubscriptionEmails(users: List[str], schedule: List[str], changes: List[str]) -> List[str]:
    sched = []
    for si, entry in enumerate(schedule):
        key, title = entry.split(",", 1)
        sched.append((si, key.strip(), title.strip()))

    plan_change = {}   # name -> (day, new_plan, order)
    renewal = {}       # name -> (day, extra, order)
    for ci, rec in enumerate(changes):
        parts = [p.strip() for p in rec.split(",")]
        name, day, kind, val = parts[0], int(parts[1]), parts[2], parts[3]
        if kind == "plan":
            plan_change[name] = (day, val, ci)
        else:
            renewal[name] = (day, int(val), ci)

    events = []  # (day, tie1, tie2, text)

    def fmt(day, title, name, plan):
        return "%d: [%s] Subscription for %s (%s)" % (day, title, name, plan)

    for ui, rec in enumerate(users):
        parts = [p.strip() for p in rec.split(",")]
        name, plan, begin, dur = parts[0], parts[1], int(parts[2]), int(parts[3])
        expiry = begin + dur

        pc = plan_change.get(name)
        rn = renewal.get(name)

        def plan_on(day):
            if pc is not None and day > pc[0]:
                return pc[1]
            return plan

        def day_of(key, exp):
            if key == "start":
                return begin
            if key == "end":
                return exp
            return exp + int(key)

        for si, key, title in sched:
            old_day = day_of(key, expiry)
            if rn is None:
                events.append((old_day, si, ui, fmt(old_day, title, name, plan_on(old_day))))
            else:
                rd, extra = rn[0], rn[1]
                new_day = day_of(key, expiry + extra)
                if old_day <= rd:
                    events.append((old_day, si, ui, fmt(old_day, title, name, plan_on(old_day))))
                if new_day > rd:
                    events.append((new_day, si, ui, fmt(new_day, title, name, plan_on(new_day))))

        if pc is not None:
            events.append((pc[0], -1, pc[2], fmt(pc[0], "Changed", name, pc[1])))
        if rn is not None:
            events.append((rn[0], -1, rn[2], fmt(rn[0], "Renewed", name, plan_on(rn[0]))))

    events.sort(key=lambda e: (e[0], e[1], e[2]))
    return [e[3] for e in events]
