# Day-by-day grid simulation: snapshot neighbor counts, apply infections and death countdowns, then resolve.
from typing import List, Optional, Any


def infectionDaysAndDeaths(grid: List[str], infectionThreshold: int, duration: int, deathThreshold: int) -> List[int]:
    rows = len(grid)
    if rows == 0:
        return [0, 0]
    cols = len(grid[0])
    if cols == 0:
        return [0, 0]

    HEALTHY, INFECTED, IMMUNE, DEAD = 0, 1, 2, 3
    state = [[HEALTHY] * cols for _ in range(rows)]
    inf_day = [[-1] * cols for _ in range(rows)]
    cd_day = [[-1] * cols for _ in range(rows)]

    for r in range(rows):
        row = grid[r]
        for c in range(cols):
            ch = row[c]
            if ch == 'X':
                state[r][c] = INFECTED
                inf_day[r][c] = 0
            elif ch == 'I':
                state[r][c] = IMMUNE
            else:
                state[r][c] = HEALTHY

    deaths = 0

    def pending() -> bool:
        for r in range(rows):
            for c in range(cols):
                if state[r][c] == INFECTED or cd_day[r][c] >= 0:
                    return True
        return False

    day = 0
    limit = rows * cols * (duration + 2) + duration + 10
    while pending() and day < limit:
        day += 1
        # neighbor counts from the start-of-day state
        counts = [[0] * cols for _ in range(rows)]
        for r in range(rows):
            for c in range(cols):
                if state[r][c] != INFECTED:
                    continue
                for dr in (-1, 0, 1):
                    rr = r + dr
                    if rr < 0 or rr >= rows:
                        continue
                    for dc in (-1, 0, 1):
                        if dr == 0 and dc == 0:
                            continue
                        cc = c + dc
                        if 0 <= cc < cols:
                            counts[rr][cc] += 1

        # simultaneous infection and countdown starts
        for r in range(rows):
            for c in range(cols):
                st = state[r][c]
                if st == IMMUNE or st == DEAD:
                    continue
                n = counts[r][c]
                if st == HEALTHY and n >= infectionThreshold:
                    state[r][c] = INFECTED
                    inf_day[r][c] = day
                if cd_day[r][c] < 0 and n >= deathThreshold:
                    cd_day[r][c] = day

        # end of day: deaths first (a countdown blocks recovery), then recoveries
        for r in range(rows):
            for c in range(cols):
                if state[r][c] == DEAD:
                    continue
                if cd_day[r][c] >= 0:
                    if cd_day[r][c] + duration <= day:
                        state[r][c] = DEAD
                        cd_day[r][c] = -1
                        inf_day[r][c] = -1
                        deaths += 1
                elif state[r][c] == INFECTED and inf_day[r][c] + duration <= day:
                    state[r][c] = IMMUNE
                    inf_day[r][c] = -1

    return [day, deaths]
