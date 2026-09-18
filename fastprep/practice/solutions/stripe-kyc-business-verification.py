# Straightforward CSV parse plus per-row rule checks (presence, length range, blocklist).
from typing import List, Optional, Any

BLOCKED = {
    "online store",
    "ecommerce",
    "retail",
    "shop",
    "general merchandise",
}


def validateBusinesses(csvData: str) -> List[str]:
    results: List[str] = []
    if not csvData:
        return results
    lines = csvData.split("\n")
    for raw in lines[1:]:
        if raw.strip() == "":
            continue
        fields = [f.strip() for f in raw.split(",")]
        name = fields[0] if fields else ""
        ok = len(fields) == 6 and all(f for f in fields)
        if ok:
            full = fields[2]
            if not (5 <= len(full) <= 31):
                ok = False
            elif full.lower() in BLOCKED:
                ok = False
        results.append(("VERIFIED: " if ok else "NOT VERIFIED: ") + name)
    return results
