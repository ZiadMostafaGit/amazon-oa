# Try flipping each next/jump instruction in turn and simulate with a visited set until one terminates.
from typing import List, Optional, Any


def _run(prog: List[tuple]) -> Optional[int]:
    n = len(prog)
    pc = 0
    acc = 0
    seen = set()
    while 0 <= pc < n:
        if pc in seen:
            return None
        seen.add(pc)
        op, val = prog[pc]
        if op == "plus":
            acc += val
            pc += 1
        elif op == "next":
            pc += 1
        else:
            pc += val
    return acc


def repairBootloader(instructions: List[str]) -> int:
    prog = []
    for line in instructions:
        parts = line.split()
        prog.append((parts[0], int(parts[1])))

    base = _run(prog)
    if base is not None:
        return base

    for i, (op, val) in enumerate(prog):
        if op == "plus":
            continue
        swapped = "jump" if op == "next" else "next"
        trial = list(prog)
        trial[i] = (swapped, val)
        res = _run(trial)
        if res is not None:
            return res
    return 0
