# Direct simulation of the tiered rack bank: lazy spent-cell purge, greedy sag equalisation, then bus-shift dispatch with inward vacancy propagation.
from typing import List, Optional, Any


class _Cell:
    __slots__ = ("cell_id", "load_ts", "duration")

    def __init__(self, cell_id, load_ts, duration):
        self.cell_id = cell_id
        self.load_ts = load_ts
        self.duration = duration

    def is_spent(self, now):
        return now - self.load_ts >= 2.0 * self.duration

    def is_charged(self, now):
        return now - self.load_ts < self.duration

    def expiry(self):
        # load_timestamp + rated_duration; ordering by this matches ordering by charge window.
        return self.load_ts + self.duration


class PowerCellBank:
    def __init__(self, num_racks: int) -> None:
        self.num_racks = num_racks
        self.racks = [[] for _ in range(num_racks)]
        self.caps = [2 ** (i + 1) for i in range(num_racks)]

    def _purge(self, now):
        for i in range(self.num_racks):
            rack = self.racks[i]
            if rack:
                self.racks[i] = [c for c in rack if not c.is_spent(now)]

    def _most_charged(self, rack, charged_only=False, now=0.0):
        best = None
        for c in rack:
            if charged_only and not c.is_charged(now):
                continue
            if best is None:
                best = c
                continue
            ce, be = c.expiry(), best.expiry()
            if ce > be or (ce == be and c.cell_id < best.cell_id):
                best = c
        return best

    def _most_depleted(self, rack):
        best = None
        for c in rack:
            if best is None:
                best = c
                continue
            ce, be = c.expiry(), best.expiry()
            if ce < be or (ce == be and c.cell_id < best.cell_id):
                best = c
        return best

    def load_cell(self, timestamp: float, cell_id: str, rated_duration: float) -> bool:
        self._purge(timestamp)
        for i in range(self.num_racks):
            if len(self.racks[i]) < self.caps[i]:
                self.racks[i].append(_Cell(cell_id, timestamp, rated_duration))
                return True
        return False

    def _equalise(self, now):
        for k in range(self.num_racks - 1):
            front = self.racks[k]
            rear = self.racks[k + 1]
            while True:
                total = len(front)
                if total == 0:
                    break
                charged = sum(1 for c in front if c.is_charged(now))
                if 2 * charged >= total:
                    break
                donor = self._most_charged(rear, charged_only=True, now=now)
                if donor is None:
                    break
                taker = self._most_depleted(front)
                if taker is None:
                    break
                front[front.index(taker)] = donor
                rear[rear.index(donor)] = taker

    def discharge(self, timestamp: float, max_dispatch: int) -> List[str]:
        self._purge(timestamp)
        self._equalise(timestamp)
        out = []
        for _ in range(max_dispatch):
            active = -1
            for i in range(self.num_racks):
                if self.racks[i]:
                    active = i
                    break
            if active < 0:
                break
            rack = self.racks[active]
            cell = self._most_charged(rack, now=timestamp)
            rack.pop(rack.index(cell))
            label = "charged" if cell.is_charged(timestamp) else "depleted"
            out.append(cell.cell_id + ":" + label)
            j = active
            while j + 1 < self.num_racks and self.racks[j + 1]:
                nxt = self.racks[j + 1]
                mover = self._most_charged(nxt, now=timestamp)
                nxt.pop(nxt.index(mover))
                self.racks[j].append(mover)
                j += 1
        return out


def powerCellBank(numRacks: int, operations: List[List[str]]) -> List[List[str]]:
    bank = PowerCellBank(numRacks)
    result = []
    for op in operations:
        if op[0] == "load_cell":
            ok = bank.load_cell(float(op[1]), op[2], float(op[3]))
            result.append(["true" if ok else "false"])
        else:
            result.append(bank.discharge(float(op[1]), int(op[2])))
    return result
