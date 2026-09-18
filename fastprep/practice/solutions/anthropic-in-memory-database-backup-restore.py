from typing import List, Optional, Any

# Persistent (immutable) treap keyed by string, giving O(log n) SET/GET/DELETE
# with full structural sharing, so BACKUP is O(1) (just keep the root) and
# RESTORE is O(1) (swap the root back in).  No map is ever copied.

# node = (key, value, priority, left, right)


def _priority(key: str) -> int:
    # deterministic pseudo-random priority derived from the key
    h = 1469598103934665603
    for ch in key:
        h ^= ord(ch)
        h = (h * 1099511628211) & 0xFFFFFFFFFFFFFFFF
    return h


def _find(node, key):
    while node is not None:
        k = node[0]
        if key == k:
            return node[1]
        node = node[3] if key < k else node[4]
    return None


def _split(node, key):
    """Split into (< key, == key node or None, > key)."""
    if node is None:
        return None, None, None
    k = node[0]
    if key < k:
        lt, eq, gt = _split(node[3], key)
        return lt, eq, (k, node[1], node[2], gt, node[4])
    if key > k:
        lt, eq, gt = _split(node[4], key)
        return (k, node[1], node[2], node[3], lt), eq, gt
    return node[3], node, node[4]


def _merge(a, b):
    if a is None:
        return b
    if b is None:
        return a
    if a[2] >= b[2]:
        return (a[0], a[1], a[2], a[3], _merge(a[4], b))
    return (b[0], b[1], b[2], _merge(a, b[3]), b[4])


def _insert(node, key, value):
    lt, _eq, gt = _split(node, key)
    fresh = (key, value, _priority(key), None, None)
    return _merge(_merge(lt, fresh), gt)


def _erase(node, key):
    """Return (new_root, existed)."""
    lt, eq, gt = _split(node, key)
    return _merge(lt, gt), eq is not None


def solveInMemoryDatabaseBackupRestore(input: str) -> List[str]:
    raw = input.split("\n") if input is not None else []
    lines = [ln.strip() for ln in raw]
    idx = 0
    while idx < len(lines) and lines[idx] == "":
        idx += 1
    if idx >= len(lines):
        return []

    first = lines[idx].split()
    idx += 1
    try:
        n = int(first[0])
    except (ValueError, IndexError):
        return []
    # tolerate the whole payload being on a single whitespace separated line
    inline_rest = first[1:]

    commands: List[List[str]] = []
    if inline_rest:
        commands = _regroup(inline_rest, n)
    else:
        while idx < len(lines) and len(commands) < n:
            if lines[idx] == "":
                idx += 1
                continue
            commands.append(lines[idx].split())
            idx += 1

    out: List[str] = []
    root = None
    backups: List[Any] = []  # backups[i] is the root snapshot for backup id i+1

    for parts in commands:
        if not parts:
            continue
        op = parts[0].upper()
        if op == "SET":
            root = _insert(root, parts[1], parts[2])
            out.append("OK")
        elif op == "GET":
            val = _find(root, parts[1])
            out.append("NULL" if val is None else val)
        elif op == "DELETE":
            root, existed = _erase(root, parts[1])
            out.append("OK" if existed else "NULL")
        elif op == "BACKUP":
            backups.append(root)
            out.append(str(len(backups)))
        elif op == "RESTORE":
            ok = False
            if len(parts) > 1:
                try:
                    bid = int(parts[1])
                except ValueError:
                    bid = 0
                if 1 <= bid <= len(backups):
                    root = backups[bid - 1]
                    ok = True
            out.append("OK" if ok else "NULL")
        else:
            out.append("NULL")
    return out


def _regroup(tokens: List[str], n: int) -> List[List[str]]:
    """Rebuild commands from a flat token stream (whitespace collapsed input)."""
    arity = {"SET": 2, "GET": 1, "DELETE": 1, "BACKUP": 0, "RESTORE": 1}
    cmds: List[List[str]] = []
    i = 0
    while i < len(tokens) and len(cmds) < n:
        op = tokens[i].upper()
        k = arity.get(op, 0)
        cmds.append(tokens[i:i + 1 + k])
        i += 1 + k
    return cmds
