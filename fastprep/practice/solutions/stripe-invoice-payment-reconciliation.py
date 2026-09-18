# Approach: CSV parsing + tiered matching (id marker > exact amount > fuzzy range), earliest due-date tie-break.
from typing import List, Optional, Any


def reconcilePayment(payment: str, invoices: List[str], forgiveness: int) -> str:
    parts = payment.split(", ")
    pay_id = parts[0].strip()
    amount = int(parts[1].strip())
    memo = ", ".join(parts[2:]) if len(parts) > 2 else ""

    parsed = []
    for inv in invoices:
        f = inv.split(", ")
        if len(f) < 3:
            f = [x.strip() for x in inv.split(",")]
        inv_id = f[0].strip()
        due = f[1].strip()
        amt = int(f[2].strip())
        parsed.append((inv_id, due, amt))

    def pick(cands):
        best = None
        for c in cands:
            if best is None or c[1] < best[1]:
                best = c
        return best

    # Tier 1: id marker in memo
    low = memo.lower()
    pos = -1
    mlen = 0
    for marker in ("paying for:", "paying off:"):
        i = low.find(marker)
        if i != -1 and (pos == -1 or i < pos):
            pos = i
            mlen = len(marker)
    if pos != -1:
        target = memo[pos + mlen:].strip()
        cands = [c for c in parsed if c[0] == target]
        if not cands:
            cands = [c for c in parsed if c[0].lower() == target.lower()]
        best = pick(cands)
        if best is not None:
            return "Payment {} paid {} for invoice {} due on {}".format(pay_id, amount, best[0], best[1])

    # Tier 2: exact amount
    best = pick([c for c in parsed if c[2] == amount])
    if best is not None:
        return "Payment {} paid {} for invoice {} due on {}".format(pay_id, amount, best[0], best[1])

    # Tier 3: fuzzy amount
    if forgiveness > 0:
        best = pick([c for c in parsed if c[2] != amount and amount - forgiveness <= c[2] <= amount + forgiveness])
        if best is not None:
            return "Payment {} paid {} for invoice {} due on {}".format(pay_id, amount, best[0], best[1])

    return "Payment {} could not be matched to any invoice".format(pay_id)
