# Simulation Problems

> Simulation is not "just do what the statement says". It is the discipline of
> choosing a state small enough to update in constant time and complete enough
> that the next event never has to look at history again.

## When you reach for it

Seven hundred and eighty-two problems in this bank are simulations, which makes
it the fifth most common topic of the hundred and fifty. That is not an accident
of tagging: most of what companies actually ask — a ledger, a queue, a rate
limiter, an in-memory filesystem, a game board — is a sequence of events and a
question about what the events did.

The trigger is a statement of this shape: **here is a list of operations;
process them in order; report what came out.** *Driver Balance Ledger* is the
purest example here. The operations are `["ADJUST", driverId, delta]`,
`["BALANCE", driverId]` and `["TOTAL"]`, and the output is the values the last
two produced. There is no insight to have; nobody is hiding a recurrence. What
is hidden is a performance clause in the statement's last line: *"The
total-balance operation may be called very frequently, so it should not scan
every driver on each call."* That sentence is the entire problem.

The families this topic covers:

- **Ledgers and account systems** — *Driver Balance Ledger*, *Financial Account
  Ledger*, *Banking System, Part 1: Accounts and Transfers* through *Part 4*,
  *GPU Credit Ledger*, *Workspace Credit Ledger*.
- **Queues and servers** — *Queue Check-in Simulation with Capacity Limit*,
  *ATM Queue Exit Order*, *Time-Ordered Elevator Dispatch*, *Priority Job
  Scheduler with Cooldowns*.
- **Automata and protocols** — *Simulate a Deterministic Finite Automaton*,
  *Circuit Breaker State Machine*, *For All Intents And Purposes Part 1* to
  *Part 3*.
- **Boards and agents** — *Cleaning Robot*, *Asteroid Collision*, *Candy Crush
  Grid Matching and Gravity*, *Falling Boxes and Exploding Obstacles*.
- **Throttles and caches** — *Token Bucket Request Decisions*, *In-Memory
  Fixed-Window Rate Limiter*, *LRU Cache with Hit and Miss Counters*, *LFU
  Cache*.
- **Event logs and replay** — *Billing Log with Undo and Redo*, *Undo and Redo
  Command History*, *Versioned Snapshot Set*, *Banking System with Historical
  Snapshots*. This family gets its own section below.

The tool is wrong in two situations, worth naming because the loop will always
*compile*.

**When there is a choice to make.** You can simulate a policy; you cannot
simulate a decision. If the statement asks for the *maximum* profit or the
*fewest* moves and you get to pick what happens next, the branching is the
problem and you want [[greedy]] or [[dynamic-programming]]. Simulation answers
"what happens", never "what is best".

**When the horizon is astronomically long.** "After 10⁹ seconds" is not a
simulation instruction unless there are also 10⁹ *events*. Cost is proportional
to the number of state transitions, not to the length of the timeline. If the
timeline is long and the state space is small, the state must repeat, and you
want [[cycle-detection]] or [[matrix-exponentiation]].

The honest anti-signal is subtler than either: simulation is always *available*,
which makes it the default that quietly runs out of budget. The question is
never "can I simulate this" but "what does one event cost me".

## The idea

Draw the events on a line and cut it anywhere.

<svg viewBox="0 0 660 190" role="img" aria-label="a timeline of events with a vertical cut; history to the left is discarded, the state sits on the cut, future events are to the right">
  <g>
    <line x1="25" y1="95" x2="635" y2="95"/>
    <circle cx="70" cy="95" r="9"/>
    <circle cx="140" cy="95" r="9"/>
    <circle cx="210" cy="95" r="9"/>
    <circle cx="280" cy="95" r="9"/>
    <circle class="fill" cx="400" cy="95" r="9"/>
    <circle class="fill" cx="470" cy="95" r="9"/>
    <circle class="fill" cx="540" cy="95" r="9"/>
    <line x1="340" y1="25" x2="340" y2="165"/>
    <rect class="fill" x="300" y="48" width="80" height="30" rx="5"/>
    <text x="340" y="42" text-anchor="middle">state</text>
    <text x="175" y="140" text-anchor="middle">processed, then forgotten</text>
    <text x="175" y="158" text-anchor="middle">(cannot be consulted again)</text>
    <text x="500" y="140" text-anchor="middle">not yet seen</text>
    <text x="500" y="158" text-anchor="middle">(must be answerable from the state)</text>
    <text x="340" y="185" text-anchor="middle">every event moves the cut one step right</text>
  </g>
</svg>

Everything left of the cut has happened and is gone; everything right is still
to come. **The state is the smallest thing you must carry across that cut so
that the future never needs to look left.** Once you have decided what sits on
the cut, the program writes itself: one function
`(state, event) → (state, output)`, and one loop that applies it.

Choosing the cut is the whole skill, and there are exactly two ways to get it
wrong.

**Too small**, and the future does have to look left — rescanning history on
every event, which is a quadratic loop. *Driver Balance Ledger* with the state
`{driver: balance}` is complete: every question is answerable. But `TOTAL`
answers itself by summing the dictionary, and over 2·10⁵ operations that sum is
the timeout.

**Too big**, and you are storing the same fact twice. The fix for `TOTAL` is to
put a redundant field on the cut: carry `total` alongside `balances`, and update
both in the one place a balance changes. That is the central move of this topic
— *cache the answer in the state and maintain it in the transition* — and it
comes with a price. You have created an invariant,

    total == sum(balances.values())

which is now yours to preserve at every write. Every simulation bug that
survives the sample cases is a derived field that drifted away from the thing it
was derived from, on some branch the samples did not take.

So the model is three lines. Pick the cut. Write one transition function. Write
down the invariant tying the redundant parts of the state to the primary parts,
because that comment is the assertion you will need at 2am.

## Worked by hand

*Queue Check-in Simulation with Capacity Limit* is the smallest problem here
that punishes a bad cut. One line, one clerk; check-in takes 30 seconds; arrival
times are non-decreasing; a person arriving when strictly more than 10 people are
already in the system — waiting *or* being served — leaves at once. For each
person, report when they start being served, or `null`.

The real constants make a hand trace unreadable, so trace it with a service time
of 3 and a limit of 1; nothing about the logic depends on the numbers. Arrivals:
`[0, 1, 2, 7, 7]`.

The state on the cut is two things: `inside`, the ascending list of finish times
of people who have not left, and `free`, the instant the clerk becomes idle. Each
arrival first evicts from `inside` everyone already finished, then decides.

| person | arrives | `inside` after evicting | in system | decision | start | finish | `free` |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 0 | 0 | `[]` | 0 | accept | 0 | 3 | 3 |
| 1 | 1 | `[3]` | 1 | accept | 3 | 6 | 6 |
| 2 | 2 | `[3, 6]` | 2 | **reject** | — | — | 6 |
| 3 | 7 | `[]` (3 and 6 popped) | 0 | accept | 7 | 10 | 10 |
| 4 | 7 | `[10]` | 1 | accept | 10 | 13 | 13 |

Output: `[0, 3, null, 7, 10]`.

Four things in that table are invisible in the code.

**The rejected person changed nothing.** Row 2 leaves `inside` and `free`
exactly as they were. The commonest wrong version computes `start = max(t, free)`
and updates `free` *before* testing the capacity, silently pushing the clerk's
schedule forward for somebody who never checked in. Everything after row 2 would
be wrong, and a sample with no rejections would still pass.

**The eviction only moves forward.** Over the whole run, `inside` is popped from
the left at most once per person. That is why a question which sounds like it
needs a scan — *how many people are in the building right now?* — costs O(1)
amortised. What licenses it is one clause of the constraints: arrivals are
non-decreasing.

**Row 4 accepts while the clerk is busy until 10.** Being in the line is not the
same as being served. A state consisting only of `free` — what people write
first, because it suffices for start times — cannot answer the capacity question
at all. That is the "too small" failure, caught by a trace rather than by
staring.

**Rows 3 and 4 share a timestamp, and their order matters.** Person 3's
acceptance is what makes person 4's count 1 rather than 0. Same-time arrivals
are enqueued in input order; the loop gets that for free by iterating over
indices, but only because the state is per-person rather than aggregated by
timestamp. Aggregate first and the tie-break is gone for good.

## Why it is correct

A simulation is correct when its state is a *sufficient statistic* for the
future: from the state alone, every later event resolves exactly as the
specification says. Proving that means writing the specification as equations,
then showing the loop maintains an invariant that implies them.

:::proof The check-in loop computes the specified schedule
**Specification.** Arrivals `a₀ ≤ a₁ ≤ … ≤ a_{n-1}`, service time `S > 0`,
capacity limit `L ≥ 0`. Define, by induction on `i`, the set `A` of accepted
people and their start times: person `i` is accepted iff

    |{ j ∈ A : j < i and s_j + S > a_i }| ≤ L

and, if accepted, `s_i = max(a_i, f_prev)` where `f_prev = s_j + S` for the
latest accepted `j < i`, or `0` if there is none. Person `j` occupies the system
over the half-open interval `[a_j, s_j + S)`, so the set counted above is exactly
"people still in the system at the instant `a_i`".

**Invariant.** At the top of the iteration that handles person `i`, before
eviction:

- **(I1)** `inside` holds, in ascending order, the finish times `s_j + S` of
  every accepted `j < i` with `s_j + S > a_{i-1}`, and nothing else;
- **(I2)** `free` equals `f_prev` as defined above;
- **(I3)** `out` holds the specified answers for persons `0 … i-1`.

**Base case.** `i = 0`: `inside`, `out` empty and `free = 0`. There is no
accepted `j < 0`, `f_prev = 0` by definition, and no answers are owed.

**Lemma (finish times ascend).** On acceptance,
`s_i + S = max(a_i, free) + S ≥ free + S > free`, and `free` is the largest
finish time in `inside`. So an appended finish time is strictly larger than every
one already there, and `inside` is always ascending. This is the only reason the
eviction loop may stop at the first element still in the future.

**Inductive step.** Assume the invariant before person `i`. Eviction pops while
`inside[0] ≤ a_i`. Since `inside` is ascending (lemma) and `a_i ≥ a_{i-1}`, the
popped elements are exactly those finish times `≤ a_i`, and by (I1) the ones left
are exactly the finish times of accepted `j < i` with `s_j + S > a_i`. Hence
`len(inside)` is precisely the cardinality the specification compares against
`L` — note `a_j ≤ a_i` for all `j < i`, so a person with unfinished service is
necessarily present rather than not yet arrived.

*Case reject* (`len(inside) > L`). The specification does not accept person `i`,
and the loop appends `None`, restoring (I3). Neither `inside` nor `free` is
written, so `A` and `f_prev` are unchanged and (I1), (I2) hold for `i + 1`.

*Case accept.* The loop sets `start = max(a_i, free)`, which by (I2) is exactly
`s_i`; appends `start + S` to `inside`, which by the lemma keeps it ascending
and by (I1) makes it the correct set for index `i + 1`; sets `free = start + S`,
which is the new `f_prev`, restoring (I2); and appends `start` to `out`,
restoring (I3).

**Termination.** The outer loop runs exactly `n` times. Each eviction pops an
element that is never re-inserted, and at most `n` elements are ever inserted, so
the eviction loop executes at most `n` times across the whole run.

**Conclusion.** After the last iteration (I3) says `out` holds the specified
answer for every person. ∎
:::

Now name what the proof used, because that list is where the bugs live.

- **Arrivals are non-decreasing.** Used twice: to stop eviction at the first
  future finish time, and to claim every unfinished accepted `j < i` has already
  arrived. Neither survives unsorted input. If a variant drops this promise, sort
  first or switch to a heap of events.
- **`S > 0`**, the source of the lemma's strict inequality.
- **Occupancy is `[a_j, s_j + S)`, half-open.** That one convention is the
  difference between `inside[0] <= t` and `inside[0] < t`, and it changes the
  answer only when a departure and an arrival share a timestamp — row 3.
- **One server, FIFO, non-preemptive.** Used in `s_i = max(a_i, free)`. With `k`
  clerks, `free` becomes a [[heap|min-heap]] of `k` finish times and the rest of
  the proof is unchanged.
- **Rejection writes nothing.** The reject branch's `i + 1` case of (I1) and (I2)
  is exactly that claim. Touch `free` there and the proof breaks at that line,
  along with the program.
- **Events are processed in index order**, which is where the tie-break for
  equal arrival times comes from, and nowhere else.

## What it costs

The cost of a simulation is a sum, not a formula:
`Σ over events of (cost of one transition)`. Deriving it means bounding the
transitions, usually with an amortised argument, because the expensive-looking
part happens rarely.

For the check-in loop, let `d_i` be the number of pops during iteration `i`, so
iteration `i` costs `c + d_i`. The total is `Σ_i (c + d_i) = cn + Σ_i d_i`, and
each pop removes an element pushed exactly once with at most one push per person,
so `Σ_i d_i ≤ n`. Total: **Θ(n)**. Equivalently, with potential
`Φ = len(inside)`, one iteration's amortised cost is
`c + d_i + (Φ_after − Φ_before) = c + d_i + (1 − d_i) = c + 1` on acceptance and
`c` on rejection — constant either way. See [[amortized-analysis]].

Compare the direct transcription, which counts the people inside by scanning
every accepted person: `Σ_i i = Θ(n²)`. At the stated `n = 2·10⁵` that is 2·10¹⁰
comparisons against 2·10⁵, and the factor comes from the state, not from
cleverness.

**Space** is `Θ(L)`, not `Θ(n)`: `inside` never holds more than `L + 1` finish
times, because an arrival that would make it larger is rejected.

Three costs people forget:

**Recomputing a derived quantity.** *Driver Balance Ledger*'s `TOTAL`: the
transition is O(1) and the query is O(drivers), so the whole run is
O(ops × drivers). Maintaining `total` incrementally makes both O(1), which is why
the statement mentions frequency at all.

**Copying the state.** Recording history by appending `dict(state)` after each
event costs `Θ(n · |state|)` — a linear simulation turned quadratic by the
logging. Store the *event*, not the state. When you genuinely need random access
to old states, checkpoint every `C` events and replay the remainder: memory
`Θ(n/C · |state|)`, lookup `Θ(C)`, and `C ≈ √n` balances them.

**Hashing the keys.** *Driver Balance Ledger*'s ids are up to 40 characters, so
every dictionary operation hashes 40 bytes. A constant factor, not a complexity
change, but a visible one over 2·10⁵ operations; interning strings to integers
once at the start is the standard fix ([[hash-tables]]).

And the cost that is not in the loop at all: **events versus timeline**. A
time-stepped simulation costs `Θ(T)`; an event-driven one jumps to the next
interesting instant and costs `Θ(E log E)`. When `T = 10⁹` and `E = 10⁵`, those
are not competing designs — one of them does not finish.

## The implementation

```python run
import random
from collections import deque


def check_in(arrivals, service=30, limit=10):
    """Start times for one FIFO clerk; None for anyone turned away.
    A person occupies the system over [arrival, finish). Someone arriving when
    strictly more than `limit` people are already inside leaves at once."""
    inside = deque()                       # finish times, ascending
    free = 0                               # the clerk is idle from here on
    out = []
    for t in arrivals:
        while inside and inside[0] <= t:   # these people have already left
            inside.popleft()
        if len(inside) > limit:
            out.append(None)               # rejected: touch nothing else
            continue
        start = t if t > free else free
        free = start + service
        inside.append(free)
        out.append(start)
    return out


def rescan(arrivals, service, limit):
    """The same rules read literally: count who is inside by scanning."""
    accepted, free, out = [], 0, []
    for t in arrivals:
        if sum(1 for s in accepted if s + service > t) > limit:
            out.append(None)
            continue
        start = max(t, free)
        free = start + service
        accepted.append(start)
        out.append(start)
    return out


small = [0, 1, 2, 7, 7]
print("arrivals               ", small)
print("service 3, limit 1  -> ", check_in(small, 3, 1))
assert check_in(small, 3, 1) == [0, 3, None, 7, 10]
print("service 30, limit 10 ->", check_in(small))
assert check_in(small) == [0, 30, 60, 90, 120]

rng = random.Random(5)
for _ in range(500):
    t, arr = 0, []
    for _ in range(rng.randint(0, 14)):
        t += rng.randint(0, 4)             # non-decreasing, with ties
        arr.append(t)
    s, L = rng.randint(1, 5), rng.randint(0, 3)
    assert check_in(arr, s, L) == rescan(arr, s, L), (arr, s, L)
print("500 random arrival streams agree with the quadratic rescan")

res = check_in(list(range(200000)))        # the stated worst case
print("200000 arrivals -> served:", sum(x is not None for x in res),
      " turned away:", sum(x is None for x in res))
```

Three lines carry the weight.

`while inside and inside[0] <= t: inside.popleft()` is the amortised eviction,
written as a loop with no bound because the bound is global, not local: one
iteration may pop ten people, but the run pops at most `n`. The `<=` rather than
`<` is the half-open convention from the proof — the only character in the
function that encodes the tie-break.

`out.append(None); continue`, before anything else is written, is the rejection
branch doing nothing. Placing the `continue` above the `start` computation is not
style; it is what makes the reject case of the invariant hold.

`start = t if t > free else free` is `max(a_i, f_prev)`: the person waits for the
clerk, or the clerk for the person, whichever is later. Every single-server
queueing simulation here has this line somewhere.

The `rescan` reference is the other half of the implementation. A simulation has
a property most algorithms do not: the specification *is* an executable program,
just a slow one. Writing it takes two minutes and turns correctness into
something you can test on five hundred random inputs rather than argue about. Do
it every time the fast version has an amortised trick in it.

## Variants you will meet

**Time-stepped versus event-driven.** Tick the clock by one unit and update
everything, or keep a priority queue of scheduled events and jump to the next
one. The first costs `Θ(T)`, the second `Θ(E log E)`. *Time-Ordered Elevator
Dispatch* and *Priority Job Scheduler with Cooldowns* are event-driven by
necessity. See [[heap]] and [[sweep-line]].

**Lazy state instead of ticking.** A rate limiter needs no background thread
refilling the bucket. Store `(tokens, last_refill)` and, on each request, add
`elapsed × rate` before deciding: the clock advances only when someone looks.
*Token Bucket Request Decisions*, *In-Memory Fixed-Window Rate Limiter* and
*Cached Lazy Token Buckets* are this trick; [[rate-limiting]] has the details.

**Event logs and replay.** The important variant, and the reason this chapter
also covers that sub-topic. Invert the relationship between state and history:
the **log is the source of truth**, and the state is nothing but a fold of the
log over an empty initial state. Everything else follows.

- *Undo* has two implementations. Replay the log's prefix from the beginning:
  always correct, `O(k)` per undo, needs nothing from the events. Or apply the
  **inverse event**: `O(1)`, but only if events are invertible — and `SET` is
  invertible only if the log entry also records the value it overwrote. *Billing
  Log with Undo and Redo*, *Undo and Redo Command History* and *Text Editor,
  Part 2: Undo and Redo* all turn on this choice.
- *Redo* is a second stack, cleared the moment a new action is performed,
  because the branch it described no longer exists.
- *Versioned reads* — "what was the value at version `v`?" — do **not** want a
  copy of the map per version. Keep, per key, an ascending list of
  `(version, value)` and [[binary-search]] it: space `Θ(total writes)` rather
  than `Θ(versions × keys)`. *Versioned Snapshot Set*, *Snapshot Map with Sparse
  Version History*, *In-Memory Database Historical Lookup* and *Banking System
  with Historical Snapshots* are all this shape. See [[persistent-structures]].
- *Replaying an at-least-once stream* means events can arrive twice, so the
  transition must be idempotent or carry a deduplication key. *Asynchronous
  Payment Event Processing* is built on that.

```python run
import random


def apply_one(state, ev):
    """Mutate `state` by `ev`; return the event that exactly undoes it."""
    kind, key = ev[0], ev[1]
    if kind == "ADJUST":
        state[key] = state.get(key, 0) + ev[2]
        return ("ADJUST", key, -ev[2])
    if kind == "SET":
        old = state.get(key, 0)           # invertible only because we read this
        state[key] = ev[2]
        return ("SET", key, old)
    raise ValueError(kind)


class Ledger:
    def __init__(self):
        self.state, self.log, self.undone = {}, [], []

    def do(self, ev):
        self.log.append((ev, apply_one(self.state, ev)))
        self.undone.clear()               # a new action kills the redo branch
        return self.state[ev[1]]

    def undo(self):
        if not self.log:
            return False
        ev, inv = self.log.pop()
        apply_one(self.state, inv)
        self.undone.append((ev, inv))
        return True

    def redo(self):
        if not self.undone:
            return False
        ev, inv = self.undone.pop()
        self.log.append((ev, apply_one(self.state, ev)))
        return True

    def replay(self):
        """The state as a fold of the log over nothing. The log is the truth."""
        s = {}
        for ev, _ in self.log:
            apply_one(s, ev)
        return s


def live(s):                              # ignore keys that are explicitly zero
    return {k: v for k, v in s.items() if v != 0}


led = Ledger()
for ev in [("ADJUST", "ana", 50), ("ADJUST", "bo", -20), ("SET", "ana", 7)]:
    led.do(ev)
print("after three events ", led.state)
led.undo()
print("after one undo     ", led.state, " replayed:", led.replay())
led.undo(); led.undo()
print("after undoing all  ", led.state, " replayed:", led.replay())
assert live(led.state) == live(led.replay()) == {}
assert led.state != led.replay(), "undo restores values, not the set of keys"

rng = random.Random(3)
for _ in range(300):
    led = Ledger()
    for _ in range(rng.randint(0, 25)):
        r = rng.random()
        if r < 0.5:
            led.do((rng.choice(["ADJUST", "SET"]), rng.choice("abc"),
                    rng.randint(-5, 5)))
        elif r < 0.8:
            led.undo()
        else:
            led.redo()
        assert live(led.state) == live(led.replay())
print("300 random do/undo/redo streams: incremental state == replay of the log")
```

The assert that looks like a typo — `led.state != led.replay()` — is the most
instructive line. Undoing every event restores every *balance* to zero, but the
incrementally-undone dictionary still holds `ana` and `bo` mapped to `0`, while
the replay never created them. The two states agree on every question the problem
can ask and are different Python objects. That gap between "equal as values" and
"equal as representations" is where undo-by-inverse and undo-by-replay diverge,
and it is worth knowing before a hidden test case iterates your dictionary.

**Automata.** When the state is one of a handful of labelled modes and the
events are symbols, the transition function is a table. *Simulate a
Deterministic Finite Automaton* hands you the table; *Circuit Breaker State
Machine* makes you write it. See [[state-machines]].

**Command-dispatch systems.** Multi-part design problems — *Banking System,
Part 1* to *Part 4*, *Cloud Storage System*, *In-Memory Database* — are
simulations whose state is an object you design. Each part adds a field, not an
algorithm. See [[design-data-structure]].

**Boards and agents.** A grid plus rules. *Cleaning Robot* walks one; *Candy
Crush Grid Matching and Gravity* alternates a match phase and a fall phase;
*Asteroid Collision* is a simulation whose correct state is a [[stack]]. See
[[matrix-traversal]].

**Skipping ahead through a cycle.** When the horizon is huge but the state small,
the sequence of states must repeat. Find the cycle, then jump `(T − μ) mod λ`
steps. *Cyclic Fuel Command Simulation* is the example; the machinery is in
[[cycle-detection]].

**Simulated concurrency.** *Metric Counter with a Fake Clock*, *Bounded
Producer–Consumer Queue* and *Blocking Keyed Cache with Waiting Readers* want
you to simulate scheduling, not to use threads: the state is a set of blocked
waiters and a deterministic wake-up rule. See [[concurrency]] and
[[producer-consumer]].

## Recognising it in a statement

Ordered by how much you should trust them.

1. **A list of typed operations, "process each in order".** `["ADJUST",
   driverId, delta]` is not a hint, it is the answer: the statement has handed
   you the transition function's signature.
2. **"Part 1", "Part 2", "Part 3" in the title.** *Banking System, Part 1*
   through *Part 4*, *Automation Pipeline, Part 1* to *Part 3*, *Account Balance
   Manager Part 1* to *Part 3*. Staged problems are always state design: each
   part adds a field and a rule.
3. **A performance clause bolted to one operation.** "…should not scan every
   driver on each call" names the field you are being asked to precompute. Read
   the last paragraph of every statement looking for that sentence.
4. **Rules written as bullets with exceptions**, plus an explicit tie-break
   ("persons arriving at the same time are enqueued in input order"). When the
   specification is that precise, the specification is the algorithm.
5. **Vocabulary of time**: ticks, rounds, turns, arrivals, "at the moment of",
   cooldown, expiry, timestamp.
6. **The output is "the state after"**, or the values produced along the way,
   rather than a maximum or a count of possibilities.

The anti-signals:

- **An optimum over choices.** You cannot simulate a decision you have not made
  yet; that is [[greedy]], [[dynamic-programming]] or [[backtracking]].
- **A horizon with no matching event count.** `10⁹` steps and `n ≤ 100` means
  closed form, cycle, or exponentiation.
- **All queries, no mutations.** If nothing changes there is no state; sort the
  queries and answer them offline ([[sweep-line]]).
- **A named structure in the statement.** "Least recently used", "priority",
  "prefix" tell you which container to use; the simulation is then trivial and
  [[lru-cache]], [[heap]] or [[trie]] is the real topic.

## Traps

**Two copies of the truth that drift apart.** A maintained `total` and the
balances it summarises; a "current top spender" and a scoreboard. Symptom:
correct for a hundred operations, then wrong after a rare branch — a deletion, a
rejection, an overwrite — that updated one and not the other. Cure: exactly one
function may write the primary state, and it updates the derived fields in the
same breath.

**Reading the state you are writing.** Demonstrated below. Symptom: the answer
depends on the direction you scanned.

**Aliasing a snapshot.** Demonstrated below. Symptom: every entry of your
history equals the final state.

**Rejected or ignored events that still move the clock.** From the trace: the
turned-away person must not advance `free`. Symptom: everything after the first
rejection is shifted.

**`<` where the statement means `≤`.** Expiry at exactly the boundary, a request
at exactly the window edge, a departure at exactly an arrival instant. Symptom:
off by one on inputs with ties, correct on everything else.

**Mutating a collection while iterating it.** Expiry sweeps written as
`for k in cache: if expired(k): del cache[k]` raise `RuntimeError` on the first
deletion. Collect the keys, then delete.

**Time-stepping something event-driven.** Symptom: samples pass, the large case
times out, and the loop body profiles clean — because the body is not the
problem, the bound is.

**Money in floats.** "Balances fit in a signed 64-bit integer" means work in
integer minor units; [[numerical-stability]] has the rest.

**Output format.** *Queue Check-in Simulation with Capacity Limit* demands the
literal lowercase token `null` for rejected people. Symptom: a perfect algorithm
marked wrong.

```python run
# One rule, two ways to step it: a cell is infected next tick if it or a
# neighbour is infected now.
def step_in_place(row):
    r = list(row)
    for i in range(len(r)):
        if r[i] == 0 and ((i and r[i - 1]) or (i + 1 < len(r) and r[i + 1])):
            r[i] = 1                      # written, then read again at i + 1
    return r


def step_double_buffer(row):
    out = list(row)
    for i in range(len(row)):
        if row[i] == 0 and ((i and row[i - 1]) or (i + 1 < len(row) and row[i + 1])):
            out[i] = 1                    # read `row`, write `out`
    return out


start = [1, 0, 0, 0, 0]
print("start          ", start)
print("in place       ", step_in_place(start), "<- crossed the whole row in one tick")
print("double buffer  ", step_double_buffer(start))
assert step_in_place(start) == [1, 1, 1, 1, 1]
assert step_double_buffer(start) == [1, 1, 0, 0, 0]
print("in place also depends on scan direction:",
      step_in_place(start[::-1])[::-1], "vs", step_in_place(start))
assert step_in_place(start[::-1])[::-1] != step_in_place(start)

# The same bug wearing a different hat: a history that is one object, n times.
alias, copies, state = [], [], {"balance": 0}
for delta in (10, -3, 5):
    state["balance"] += delta
    alias.append(state)                   # a reference, not a snapshot
    copies.append(dict(state))            # the value at this instant
print("aliased history", alias)
print("copied history ", copies)
assert alias == [{"balance": 12}] * 3
assert copies == [{"balance": 10}, {"balance": 7}, {"balance": 12}]
print("every aliased entry is the final state; only the copies are history")
```

Both halves of that block are the same mistake: the code assumed it held a value
when it held a place in memory. `dict(state)` fixes the second only while the
state is flat — nested state needs `copy.deepcopy`, at which point the cost
argument above should push you back to storing events instead of snapshots.

## What to memorise

Almost nothing, because this topic has no formula. Three habits and a shape.

**The shape.** One state object, one transition function, one loop:

```python
state = fresh()
out = []
for ev in events:
    kind, args = ev[0], ev[1:]
    result = HANDLERS[kind](state, *args)   # one place per operation
    if result is not None:
        out.append(result)
```

A dispatch dictionary rather than a chain of `if`s, because the multi-part
problems here grow by adding operations, and a chain of `if`s grows by adding
places to forget a counter.

**The sentence** that turns a statement into that shape: *"What is the smallest
thing I must carry across the line between the events I have processed and the
ones I have not?"* Answer it in words before typing. If the answer contains "and
then I look back at the earlier events", you have not answered it yet.

**The habit**: write every derived field's invariant as an assertion, run the
random test against a literal transcription of the specification, and only then
delete the assertion. Simulations are not hard to think about; they are hard to
keep consistent, and consistency is what assertions check.

Numbers worth carrying: 2·10⁵ operations with an O(n) rescan inside is 4·10¹⁰
steps and will not finish; with an O(1) transition it is 2·10⁵. Checkpoint every
`√n` events when you need random access to history. A state space of size `k`
run for `T ≫ k` steps must repeat within `k` steps.

## Check yourself

:::check
The eviction loop in `check_in` has no bound — one iteration can pop any number
of people. Why is the whole function still linear, and which line of the problem
statement is what makes the argument work?
--
Because the bound is global rather than per-iteration. Every pop removes a
finish time that was pushed exactly once, and at most one push happens per
person, so the run performs at most `n` pops. Formally, with `Φ = len(inside)`
the amortised cost of an iteration is `c + d_i + (Φ_after − Φ_before)` — that is
`c + 1` on acceptance (one push, `d_i` pops, net change `1 − d_i`) and `c` on
rejection.

The load-bearing line of the statement is *"arrivalTimes is non-decreasing"*.
Ascending arrivals plus ascending finish times are what make the departed always
a prefix, so the loop may stop at the first element still in the future. With
unsorted arrivals, `inside[0] > t` no longer implies nothing further along has
finished, and the count is wrong, not merely slow.
:::

:::check
Someone says: "simulation problems have no algorithm — you just write what the
statement says, so they are the easy ones." Where are they wrong?
--
They are right that there is no *insight* and wrong that there is no *design*.
The literal transcription of the statement is easy to write and usually
quadratic: *Driver Balance Ledger*'s `TOTAL` reads every driver, *Queue
Check-in*'s capacity rule counts everyone accepted so far. Both statements
contain a sentence about how often the expensive operation is called, and that
sentence is the problem.

What you design is the *state*: which facts cross the cut, and which derived
quantities are maintained rather than recomputed. That is where the complexity
lives and where every surviving bug lives, because each maintained quantity is
an invariant you now owe.

They are also wrong about difficulty. Some of the hardest problems here —
*In-Memory Database*, *Limit Order Book Matching Engine*, *Banking System, Part
4* — are simulations. Nothing in them is clever; all of them are long, and long
is its own kind of hard.
:::

:::check
You are implementing undo for *Billing Log with Undo and Redo*. When should you
store inverse events, and when should you replay the log from the start? What
does a hybrid cost?
--
Store inverses when every operation is invertible with information you can
capture as it is applied. `ADJUST(k, d)` inverts to `ADJUST(k, −d)` for free;
`SET(k, v)` inverts to `SET(k, old)` only if the log entry records `old`. Then
undo is O(1) at unbounded depth. It fails when an operation destroys information
you cannot afford to save — clearing a large collection, whose inverse is the
whole collection.

Replay from the start when operations are not invertible, or when the state is
small enough that an O(k) rebuild is free. It is also the obviously correct
version, which makes it the right reference to test the fast one against.

The hybrid is checkpointing: a full copy every `C` events, rebuilding any prefix
from the nearest checkpoint plus at most `C` events. Memory `Θ((n/C)·|state|)`,
lookup `Θ(C)`, balanced at `C ≈ √n`. For *sparse* per-key history an ascending
`(version, value)` list per key plus a binary search beats it on both axes.
:::

:::check
In the worked trace, person 4 is accepted at time 7 even though the clerk is
busy until time 10. Suppose someone simplifies the state down to just `free`,
the instant the clerk next becomes idle, arguing that it determines every start
time. What breaks, and what does that tell you about choosing state?
--
Start times survive: `s_i = max(a_i, free)` needs nothing else. The capacity rule
does not. "More than 10 people in the system" counts everyone between their
arrival and their finish — the queue plus the person being served — and `free` is
one number that cannot tell one person being served from eleven queued behind
them. Person 4 would look identical to a person arriving at time 7 behind twelve
others.

The lesson is the cut. `free` is sufficient for the *future of the clerk* and
insufficient for the *future of the queue*, and a state must be sufficient for
every question the remaining events can ask, not just the one you thought of
first. The cheap way to find out is the hand trace: pick two histories that
collapse to the same state and check the statement really cannot tell them apart.
:::

:::check
A colleague implementing *Versioned Snapshot Set* says: "a snapshot has to be a
copy of the whole set, so `k` snapshots of `n` keys cost `O(nk)` — there is no
way around it." Where are they wrong?
--
They have confused a snapshot with a copy. A snapshot only has to be a *name for
an instant*, and the instant is recoverable from the write history.

Keep a global version counter that increments on each snapshot, and per key an
ascending list of `(version, value)` recording only the versions at which that
key actually changed. A read at version `v` is a binary search for the last entry
with version `≤ v`. Memory is `Θ(W)` for `W` writes — independent of the number
of snapshots and of how many keys were untouched between them. The trade is that
a read costs `Θ(log W_k)` instead of `Θ(1)`.

Their `O(nk)` is right only for the strategy they assumed — the one that turns a
linear simulation quadratic just by observing it, which is the general reason to
log events rather than states.
:::
