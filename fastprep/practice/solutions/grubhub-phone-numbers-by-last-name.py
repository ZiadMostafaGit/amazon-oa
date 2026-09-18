# Linear scan: split each record at the final ", " and compare the last name token.
from typing import List, Optional, Any


def phoneNumbersByLastName(records: List[str], lastName: str) -> List[str]:
    out: List[str] = []
    for rec in records:
        idx = rec.rfind(", ")
        if idx == -1:
            continue
        names = rec[:idx].split()
        phone = rec[idx + 2:].strip()
        if names and names[-1] == lastName:
            out.append(phone)
    return out
