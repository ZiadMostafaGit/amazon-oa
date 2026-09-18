# Simulation: seat/wait FIFO queue with lazy deletion, pay-once flags.
from collections import deque
from typing import List


def computeDayGains(nbSeats: int, payingGuests: List[int], guestMovements: List[int]) -> int:
    n = len(payingGuests)
    OUTSIDE, SEATED, WAITING = 0, 1, 2
    state = [OUTSIDE] * n
    paid = [False] * n
    free = nbSeats
    line = deque()
    total = 0

    for g in guestMovements:
        if state[g] == OUTSIDE:
            # arrival
            if free > 0:
                free -= 1
                state[g] = SEATED
            else:
                state[g] = WAITING
                line.append(g)
        elif state[g] == WAITING:
            # departure from the waiting line: no payment, lazily removed
            state[g] = OUTSIDE
        else:
            # departure from a seat
            state[g] = OUTSIDE
            if not paid[g]:
                paid[g] = True
                total += payingGuests[g]
            # the earliest still-waiting guest takes the freed seat
            while line and state[line[0]] != WAITING:
                line.popleft()
            if line:
                nxt = line.popleft()
                state[nxt] = SEATED
            else:
                free += 1
    return total
