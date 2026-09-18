# Single pass over events with an event-id dedupe set and a dict of payment state records.
from typing import List


def processEvents(events: List[str]) -> List[str]:
    seen = set()
    payments = {}
    order = []
    for row in events:
        parts = row.split(",")
        if len(parts) != 7:
            continue
        event_id, event_time, _etype, payment_id, ptype, merchant_id, amount = parts
        if event_id in seen:
            continue
        seen.add(event_id)
        if ptype == "create":
            if payment_id in payments:
                continue
            payments[payment_id] = {
                "merchant": "" if merchant_id == "-" else merchant_id,
                "state": "created",
                "auth": 0,
                "cap": 0,
                "last": event_time,
            }
            order.append(payment_id)
            continue
        rec = payments.get(payment_id)
        if rec is None:
            continue
        if ptype == "authorize":
            rec["auth"] += int(amount)
            rec["state"] = "authorized"
        elif ptype == "capture":
            rec["cap"] += int(amount)
            rec["state"] = "successful" if rec["cap"] == rec["auth"] else "partially_captured"
        else:
            continue
        rec["last"] = event_time
    out = []
    for pid in order:
        r = payments[pid]
        out.append("%s,%s,%s,%d,%d,%s" % (pid, r["merchant"], r["state"], r["auth"], r["cap"], r["last"]))
    return out
