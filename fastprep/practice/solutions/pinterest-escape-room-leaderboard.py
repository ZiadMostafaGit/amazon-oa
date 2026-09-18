# Approach: bucket players by room in insertion-ordered dicts; leaderboard scans rooms top-down until k collected.
from typing import List, Optional, Any


def runEscapeRoomLeaderboard(players: List[str], roomCount: int, operations: List[str]) -> List[str]:
    rooms = [dict() for _ in range(roomCount + 1)]
    where = {}
    for p in players:
        rooms[0][p] = True
        where[p] = 0

    results = []
    for op in operations:
        space = op.find(' ')
        if space == -1:
            name, arg = op, ''
        else:
            name, arg = op[:space], op[space + 1:]

        if name == 'ADVANCE':
            r = where[arg]
            if r < roomCount:
                del rooms[r][arg]
                r += 1
                where[arg] = r
                rooms[r][arg] = True
            results.append(str(r))
        elif name == 'GET':
            results.append(str(where[arg]))
        else:  # LEADERBOARD
            k = int(arg)
            picked = []
            if k > 0:
                for r in range(roomCount, -1, -1):
                    bucket = rooms[r]
                    if not bucket:
                        continue
                    for p in bucket:
                        picked.append(p)
                        if len(picked) == k:
                            break
                    if len(picked) == k:
                        break
            results.append(','.join(picked))
    return results
