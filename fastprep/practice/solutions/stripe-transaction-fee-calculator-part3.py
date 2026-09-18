# CSV scan keeping a running completed-volume counter per (merchant, provider) pair.
import math
from typing import List, Optional, Any


def calculateFeesWithWaiver(csvData: str, feeRules: List[str]) -> List[str]:
    rules = {}
    for rule in feeRules or []:
        rule = rule.strip()
        if not rule:
            continue
        parts = rule.split(",")
        rules[parts[0].strip()] = (float(parts[1]), float(parts[2]))

    lines = [ln for ln in (csvData or "").split("\n") if ln.strip() != ""]
    out = ["id,transaction_type,payment_provider,fee"]
    if not lines:
        return out

    header = [h.strip() for h in lines[0].split(",")]
    idx = {name: i for i, name in enumerate(header)}
    volume = {}

    for line in lines[1:]:
        cells = line.split(",")
        tid = cells[idx["id"]].strip()
        amount = int(cells[idx["amount"]].strip())
        ttype = cells[idx["transaction_type"]].strip()
        provider = cells[idx["payment_provider"]].strip()
        status = cells[idx["status"]].strip()
        merchant = cells[idx["merchant_id"]].strip()

        fee = 0
        if status == "payment_completed":
            key = (merchant, provider)
            seen = volume.get(key, 0)
            if seen > 10000:
                fee = 0
            else:
                rate, fixed = rules.get(provider, (0.0, 0.0))
                fee = math.floor(amount * rate + fixed)
                volume[key] = seen + amount
        out.append("%s,%s,%s,%d" % (tid, ttype, provider, fee))
    return out
