# Event simulation over a 30-day cycle with exact integer arithmetic (costs scaled by 30) plus marginal tier pricing.
from typing import List, Optional, Any


def calculateMonthlyCharges(subscriptions: List[str], changes: List[str], pricing: List[str], usage: List[str]) -> List[List[str]]:
    users = set()
    # sub_id -> [user, cost, start_day, ended]
    subs = {}
    for row in subscriptions:
        uid, sid, cost = row.split(",")
        users.add(uid)
        subs[sid] = [uid, int(cost), 1, False]

    parsed_changes = []
    for row in changes:
        uid, old_id, new_id, new_cost, day = row.split(",")
        uid = uid.strip()
        old_id = old_id.strip()
        new_id = new_id.strip()
        users.add(uid)
        parsed_changes.append((int(day), uid, old_id, new_id, int(new_cost)))
    parsed_changes.sort(key=lambda c: c[0])

    scaled = {}  # user -> sum(cost * days_active)
    for day, uid, old_id, new_id, new_cost in parsed_changes:
        if old_id != "-" and old_id in subs:
            rec = subs[old_id]
            if not rec[3]:
                rec[3] = True
                days = day - rec[2]
                if days > 0:
                    scaled[rec[0]] = scaled.get(rec[0], 0) + rec[1] * days
        subs[new_id] = [uid, new_cost, day, False]

    for rec in subs.values():
        if not rec[3]:
            days = 31 - rec[2]
            if days > 0:
                scaled[rec[0]] = scaled.get(rec[0], 0) + rec[1] * days

    # tiers: product -> sorted list of (upper_bound, unit_price), unlimited last
    tiers = {}
    for row in pricing:
        pid, bound, price = row.split(",")
        tiers.setdefault(pid, []).append((int(bound), int(price)))
    for pid in tiers:
        finite = sorted((b, p) for b, p in tiers[pid] if b >= 0)
        unlimited = [(b, p) for b, p in tiers[pid] if b < 0]
        tiers[pid] = finite + unlimited

    totals_usage = {}
    agg = {}
    for row in usage:
        uid, pid, qty = row.split(",")
        users.add(uid)
        agg[(uid, pid)] = agg.get((uid, pid), 0) + int(qty)

    for (uid, pid), qty in agg.items():
        cost = 0
        prev = 0
        remaining = qty
        for bound, price in tiers.get(pid, []):
            if remaining <= 0:
                break
            if bound < 0:
                cost += remaining * price
                remaining = 0
            else:
                take = min(remaining, bound - prev)
                if take > 0:
                    cost += take * price
                    remaining -= take
                prev = bound
        totals_usage[uid] = totals_usage.get(uid, 0) + cost

    result = []
    for uid in sorted(users):
        total = scaled.get(uid, 0) + totals_usage.get(uid, 0) * 30
        result.append([uid, str(total // 30)])
    return result
