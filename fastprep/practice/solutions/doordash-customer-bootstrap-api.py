# Approach: deterministic retry loop per service over the response schedule with timeout/terminal/retryable classification.
from typing import List, Optional, Any


def _resolve(service: str, timeoutMs: int, maxAttempts: int, table: dict) -> Optional[str]:
    for attempt in range(1, maxAttempts + 1):
        row = table.get((service, attempt))
        if row is None:
            continue  # timeout -> retryable
        latency = int(row[2])
        status = int(row[3])
        value = row[4]
        if latency > timeoutMs:
            continue
        if status == 200:
            return value
        if 500 <= status <= 599:
            continue
        return None  # terminal
    return None


def bootstrapCustomer(email: str, timeoutMs: int, maxAttempts: int, responses: List[List[str]]) -> List[str]:
    table = {}
    for row in responses:
        table[(row[0], int(row[1]))] = row

    customer = _resolve("USER", timeoutMs, maxAttempts, table)
    if customer is None:
        return ["", "", ""]
    card = _resolve("PAYMENT", timeoutMs, maxAttempts, table)
    addr = _resolve("ADDRESS", timeoutMs, maxAttempts, table)
    return [customer,
            card if card is not None else "UNKNOWN_CARD",
            addr if addr is not None else "UNKNOWN_ADDRESS"]
