# Parse both objects, apply the per-key merge rule, then re-emit compact JSON with sorted keys.
import json


def mergeJson(baseJson: str, incomingJson: str, behavior: str) -> str:
    base = json.loads(baseJson)
    incoming = json.loads(incomingJson)
    merged = {k: list(v) for k, v in base.items()}
    for key, arr in incoming.items():
        if behavior == "APPEND" and key in merged:
            merged[key].extend(arr)
        else:
            merged[key] = list(arr)
    parts = []
    for key in sorted(merged):
        parts.append(json.dumps(key) + ":[" + ",".join(str(x) for x in merged[key]) + "]")
    return "{" + ",".join(parts) + "}"
