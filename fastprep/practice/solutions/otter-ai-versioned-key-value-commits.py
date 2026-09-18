# Dictionary working state plus an append-only list of committed snapshots.
from typing import List, Optional, Any


def versionedStore(operations: List[str]) -> List[str]:
    state = {}
    versions = []
    out = []
    for op in operations:
        parts = op.split()
        if not parts:
            continue
        cmd = parts[0].upper()
        if cmd == 'SET':
            state[parts[1]] = parts[2]
        elif cmd == 'GET':
            out.append(state.get(parts[1], 'NULL'))
        elif cmd == 'DELETE':
            state.pop(parts[1], None)
        elif cmd == 'COMMIT':
            versions.append(dict(state))
            out.append(str(len(versions) - 1))
        elif cmd == 'ROLLBACK':
            vid = int(parts[1])
            state = dict(versions[vid])
            out.append('OK')
    return out
