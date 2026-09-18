# Command interpreter: dictionary of datacenters plus Haversine distance sorting for routing.
import math
from typing import List

EARTH_RADIUS = 6371.0


def _parse_coord(text: str, limit: float) -> float:
    value = float(text)
    if math.isnan(value) or math.isinf(value):
        raise ValueError("bad coordinate")
    if value < -limit or value > limit:
        raise ValueError("out of range")
    return value


def _haversine(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    p1, p2 = math.radians(lat1), math.radians(lat2)
    dphi = p2 - p1
    dlam = math.radians(lon2 - lon1)
    a = math.sin(dphi / 2) ** 2 + math.cos(p1) * math.cos(p2) * math.sin(dlam / 2) ** 2
    return 2 * EARTH_RADIUS * math.asin(min(1.0, math.sqrt(a)))


def _round_km(value: float) -> int:
    return int(math.floor(value + 0.5))


def solveRequestRoutingSystem(input: str) -> List[str]:
    centers = {}  # name -> [lat, lon, capacity, healthy, load]
    out = []
    for raw in input.split("\n"):
        line = raw.strip()
        if not line:
            continue
        parts = line.split()
        cmd = parts[0]
        try:
            if cmd == "REGISTER":
                if len(parts) != 5:
                    raise ValueError("arity")
                name = parts[1]
                if name in centers:
                    raise ValueError("duplicate")
                lat = _parse_coord(parts[2], 90.0)
                lon = _parse_coord(parts[3], 180.0)
                capacity = int(parts[4])
                if capacity <= 0:
                    raise ValueError("capacity")
                centers[name] = [lat, lon, capacity, True, 0]
                out.append("OK")
            elif cmd == "SET_HEALTHY":
                if len(parts) != 3:
                    raise ValueError("arity")
                name = parts[1]
                if name not in centers:
                    raise ValueError("unknown")
                flag = parts[2].lower()
                if flag not in ("true", "false"):
                    raise ValueError("flag")
                centers[name][3] = flag == "true"
                out.append("OK")
            elif cmd == "DISTANCE":
                if len(parts) != 5:
                    raise ValueError("arity")
                lat1 = _parse_coord(parts[1], 90.0)
                lon1 = _parse_coord(parts[2], 180.0)
                lat2 = _parse_coord(parts[3], 90.0)
                lon2 = _parse_coord(parts[4], 180.0)
                out.append(str(_round_km(_haversine(lat1, lon1, lat2, lon2))))
            elif cmd == "ROUTE":
                if len(parts) != 3:
                    raise ValueError("arity")
                lat = _parse_coord(parts[1], 90.0)
                lon = _parse_coord(parts[2], 180.0)
                healthy = [
                    (_haversine(lat, lon, info[0], info[1]), name)
                    for name, info in centers.items()
                    if info[3]
                ]
                if not healthy:
                    out.append("None")
                else:
                    healthy.sort()
                    candidates = ",".join(name for _, name in healthy)
                    chosen = None
                    for dist, name in healthy:
                        info = centers[name]
                        if info[4] < info[2]:
                            info[4] += 1
                            chosen = (name, dist)
                            break
                    if chosen is None:
                        out.append("None " + candidates)
                    else:
                        out.append(
                            "%s %d %s" % (chosen[0], _round_km(chosen[1]), candidates)
                        )
            else:
                out.append("ERROR")
        except (ValueError, IndexError):
            out.append("ERROR")
    return out
