# Per-camera FIFO deques for commands and logs, replayed over the operation list.
from typing import List, Optional, Any
from collections import deque


def cameraLogApiSequence(cameraIds: List[str], initialCommands: List[List[str]], initialLogs: List[List[str]], operationTypes: List[str], operationCameraIds: List[str], operationPayloads: List[str]) -> List[str]:
    commands = {}
    logs = {}
    for i, cid in enumerate(cameraIds):
        commands[cid] = deque(initialCommands[i] if i < len(initialCommands) else [])
        logs[cid] = deque(initialLogs[i] if i < len(initialLogs) else [])
    out: List[str] = []
    for i, op in enumerate(operationTypes):
        cid = operationCameraIds[i]
        if cid not in commands:
            commands[cid] = deque()
            logs[cid] = deque()
        if op == "POLL_COMMAND":
            q = commands[cid]
            out.append(q.popleft() if q else "NONE")
        elif op == "GET_LOG":
            q = logs[cid]
            out.append(q.popleft() if q else "NONE")
        else:
            logs[cid].append(operationPayloads[i])
            out.append("ACK")
    return out
