# Manual tokenizer: split top-level commas while tracking bracket depth, then map keys.
from typing import List, Optional, Any


def _split_top_level(text: str) -> List[str]:
    parts = []
    depth = 0
    current = []
    for ch in text:
        if ch == '[':
            depth += 1
            current.append(ch)
        elif ch == ']':
            depth -= 1
            current.append(ch)
        elif ch == ',' and depth == 0:
            parts.append(''.join(current))
            current = []
        else:
            current.append(ch)
    parts.append(''.join(current))
    return parts


def parseRecord(encodedRecord: str, machineEnum: List[str], keyMap: List[str]) -> List[str]:
    record = ''.join(ch for ch in encodedRecord if not ch.isspace())

    enum_map = {}
    for entry in machineEnum or []:
        cleaned = ''.join(ch for ch in entry if not ch.isspace())
        if '=' in cleaned:
            code, name = cleaned.split('=', 1)
            enum_map[code] = name

    key_map = {}
    for entry in keyMap or []:
        cleaned = ''.join(ch for ch in entry if not ch.isspace())
        if '=' in cleaned:
            src, dst = cleaned.split('=', 1)
            key_map[src] = dst

    fields = record.split(',', 4)
    machine_code = fields[0]
    timestamp = fields[1] if len(fields) > 1 else ''
    field1 = fields[2] if len(fields) > 2 else ''
    field2 = fields[3] if len(fields) > 3 else ''
    block = fields[4] if len(fields) > 4 else ''

    start = block.find('$[')
    end = block.rfind(']&')
    body = block[start + 2:end] if start != -1 and end != -1 and end > start else ''

    out = ['machine_code=' + enum_map.get(machine_code, machine_code),
           'timestamp=' + timestamp,
           'field1=' + field1,
           'field2=' + field2]

    if body:
        for entry in _split_top_level(body):
            if not entry:
                continue
            idx = entry.find(':')
            if idx == -1:
                key, value = entry, ''
            else:
                key, value = entry[:idx], entry[idx + 1:]
            out.append(key_map.get(key, key) + '=' + value)
    return out
