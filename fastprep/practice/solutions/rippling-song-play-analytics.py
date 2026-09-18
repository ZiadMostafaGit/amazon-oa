# Simulation: per-song listener sets plus an ordered-dict recency list per user.
from typing import List, Optional, Any
from collections import OrderedDict


def runSongAnalytics(operations: List[List[str]]) -> List[List[str]]:
    names = {}          # song id -> name
    listeners = {}      # song id -> set of user ids
    recent = {}         # user id -> OrderedDict of song name -> None (oldest first)
    next_id = 1
    out = []
    for op in operations:
        kind = op[0]
        if kind == "ADD_SONG":
            song_id = next_id
            next_id += 1
            names[song_id] = op[1]
            listeners[song_id] = set()
            out.append([str(song_id)])
        elif kind == "PLAY":
            song_id = int(op[1])
            user = op[2]
            listeners[song_id].add(user)
            hist = recent.get(user)
            if hist is None:
                hist = OrderedDict()
                recent[user] = hist
            name = names[song_id]
            if name in hist:
                hist.move_to_end(name)
            else:
                hist[name] = None
        elif kind == "ANALYTICS":
            rows = [(names[sid], len(listeners[sid])) for sid in names]
            rows.sort(key=lambda p: (-p[1], p[0]))
            out.append(["%s(%d)" % (name, cnt) for name, cnt in rows])
        elif kind == "RECENT":
            user = op[1]
            k = int(op[2])
            hist = recent.get(user)
            if hist is None:
                out.append([])
            else:
                items = list(hist.keys())
                items.reverse()
                out.append(items[:k])
    return out
